from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm ,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from rest_framework import viewsets,permissions
from .serializers import TweetSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.
def index(request):
    return render(request,"index.html")

def tweet_list(request):
    query =  request.GET.get('q')
    if query:
        tweets = Tweet.objects.filter(Q(text__icontains=query)).order_by('-created_at')
    else:
        tweets =Tweet.objects.all().order_by('created_at')

    return render(request,'tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
    if request.method == "POST":
        form=TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
            

    else:
        form = TweetForm()
    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_edit(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id, user = request.user)
    if request.method =="POST":
         form=TweetForm(request.POST,request.FILES,instance=tweet)
         if form.is_valid():
             tweet = form.save(commit= False)
             tweet.user = request.user
             tweet.save()
             return redirect('tweet_list')

    else:
        form = TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_delete(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet': tweet})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # optional but safe
            user.save()
            login(request, user)  # auto login
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()  # ← This fixes the bug!

    return render(request, 'registration/register.html', {'form': form})

def like_tweet(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id)

    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)
    

    return redirect('tweet_list')

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['get'])
    def mytweets(self, request):
        tweets = Tweet.objects.filter(user=request.user)
        serializer = self.get_serializer(tweets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_like(self, request, pk=None):
        tweet = self.get_object()
        user = request.user
        
        if user in tweet.likes.all():
            tweet.likes.remove(user)
            liked = False
        else:
            tweet.likes.add(user)
            liked = True
            
        return Response({'liked': liked, 'total_likes': tweet.likes.count()})

    
