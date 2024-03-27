from django.shortcuts import render, HttpResponse

from .models import Post, Tag

def home(request):
    posts = Post.objects.filter(active=True, featured=True)[0:3]

    context = {'posts':posts}
    return render(request, 'homepage/index.html', context)

def posts(request):

    posts = Post.objects.filter(active=True)

    context = {'posts': posts}

    return render(request, 'homepage/posts.html', context)

def post(request, pk):
    post = Post.objects.get(id=pk)

    context = {'post':post}
    return render(request, 'homepage/post.html', context)

def profile(request):
    return render(request, 'homepage/profile.html')
