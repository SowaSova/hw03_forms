from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User

POSTS_ON_PAGE = 10


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group_template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, group_template, context)


def profile(request, username):
    profile_template = 'posts/profile.html'
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = Post.objects.filter(author=user).count()
    context = {
        'page_obj': page_obj,
        'author': user,
        'count': count
    }
    return render(request, profile_template, context)


def post_detail(request, post_id):
    post_detail_template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    pub_date = post.pub_date
    text = post.text
    title_text = text[:30]
    author = post.author
    post_count = author.posts.all().count()
    group = post.group
    context = {
        'post': post,
        'title_text': title_text,
        'text': text,
        'author': author,
        'post_count': post_count,
        'group': group,
        'pub_date': pub_date,
    }
    return render(request, post_detail_template, context)


@login_required
def post_create(request):
    create_post_template = 'posts/create_post.html'
    group = Group.objects.all()
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('posts:profile', username=request.user.username)

    context = {
        'form': form,
        'group': group
    }
    return render(request, create_post_template, context)


def post_edit(request, post_id):
    post_edit_template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post.id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post.id)
    context = {
        'form': form,
        'post': post,
        'is_edit': True
    }
    return render(request, post_edit_template, context)
