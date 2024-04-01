from django.shortcuts import render, HttpResponse, redirect
from .models import Post, Tag
from .forms import PostForm
from .filters import PostFilter
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def home(request):
    posts = Post.objects.filter(active=True, featured=True)[0:3]

    context = {'posts':posts}
    return render(request, 'homepage/index.html', context)

def posts(request):
    posts = Post.objects.filter(active=True)
    myfilter = PostFilter(request.GET, queryset=posts)
    posts = myfilter.qs

    page = request.GET.get('page')

    paginator = Paginator(posts, 3)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts':posts, 'myfilter':myfilter}
    return render(request, 'homepage/posts.html', context)

def post(request, slug):
    post = Post.objects.get(slug=slug)

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
def updatePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts')

    context = {'form':form}
    return render(request, 'homepage/post_form.html', context)


@login_required(login_url="home")
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')

    context = {'post':post}

    return render(request, 'homepage/delete.html', context)


def sendEmail(request):

    if request.method == 'POST':

        template = render_to_string('homepage/email_template.html', {
            'name':request.POST['name'],
            'email':request.POST['email'],
            'message':request.POST['message']
        })

        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['giokhomaa@gmail.com']
        )

        email.fail_silently=False
        email.send()
    return render(request, 'homepage/email_sent.html')










