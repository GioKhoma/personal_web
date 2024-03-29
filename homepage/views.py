from django.shortcuts import render, HttpResponse, redirect
from .models import Post, Tag
from .forms import PostForm
from .filters import PostFilter
from django.contrib.auth.decorators import login_required

def home(request):
    posts = Post.objects.filter(active=True, featured=True)[0:3]

    context = {'posts':posts}
    return render(request, 'homepage/index.html', context)

def posts(request):
    posts = Post.objects.filter(active=True)
    myfilter = PostFilter(request.GET, queryset=posts)
    posts = myfilter.qs

    context = {'posts': posts, 'myfilter':myfilter}
    return render(request, 'homepage/posts.html', context)

def post(request, pk):
    post = Post.objects.get(id=pk)

    context = {'post':post}
    return render(request, 'homepage/post.html', context)

def profile(request):
    return render(request, 'homepage/profile.html')


#CRUD VIEWS
#@admin_only
@login_required(login_url="home")
def createPost(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('posts')

    context = {'form':form}
    return render(request, 'homepage/post_form.html', context)


@login_required(login_url="home")
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts')

    context = {'form':form}
    return render(request, 'homepage/post_form.html', context)


@login_required(login_url="home")
def deletePost(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')

    context = {'post':post}

    return render(request, 'homepage/delete.html', context)










