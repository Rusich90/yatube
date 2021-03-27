from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Group, User, Follow
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView
)




# def index(request):
#     post_list = Post.objects.all()
#     paginator = Paginator(post_list, 10)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#     context = {
#         'page': page,
#         'paginator': paginator,
#     }
#     return render(request, 'index.html', context)


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    paginate_by = 10


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_post_list = group.posts.all()
    paginator = Paginator(group_post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "group": group,
        'page': page,
        'paginator': paginator,
    }

    return render(request, "group.html", context)


# class GroupView(ListView):
#     model = Group

@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'new_post.html', {"form": form})
    text = form.cleaned_data['text']
    group = form.cleaned_data['group']
    image = form.cleaned_data['image']
    Post.objects.create(author=request.user, group=group, text=text, image=image)
    return redirect('index')


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    profile_post_list = profile.posts.all()
    paginator = Paginator(profile_post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = False
    if request.user.is_authenticated:
        following = request.user.follower.filter(author=profile).exists()
    context = {
        "profile": profile,
        'page': page,
        'paginator': paginator,
        'following': following
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=profile, pk=post_id)
    post_list = profile.posts.all()
    form = CommentForm(instance=None)
    comments = post.comments.all()
    paginator = Paginator(comments, 10)
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)
    context = {
        'items': items,
        'form': form,
        'post': post,
        'post_list': post_list,
        'paginator': paginator
    }

    return render(request, 'post.html', context)


# class PostView(DetailView):
#     model = Post
#     template_name = 'post.html'
#     slug_url_kwarg = 'username'
#     pk_url_kwarg = 'post_id'

@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)
    if not form.is_valid():
        return render(request, 'new_post.html', {"form": form, "post": post})
    form.save()
    return redirect('post', username=request.user.username, post_id=post_id)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('post', username=username, post_id=post_id)


@login_required
def follow_index(request):
    fav_posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(fav_posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'follow.html', context)

@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author == request.user:
        return redirect(reverse('profile', kwargs={'username': username}))
    if request.user.follower.filter(author=author).exists():
        return redirect(reverse('profile', kwargs={'username': username}))
    Follow.objects.create(author=author, user=request.user)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    profile = get_object_or_404(User, username=username)
    follow = Follow.objects.get(author=profile, user=request.user)
    follow.delete()
    return redirect('profile', username=username)


def page_not_found(request, exeption):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
