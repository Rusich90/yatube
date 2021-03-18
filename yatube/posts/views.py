from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Group, User
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_post_list = group.posts.all()
    paginator = Paginator(group_post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "group.html", {"group": group, 'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'new_post.html', {"form": form})
    text = form.cleaned_data['text']
    group = form.cleaned_data['group']
    Post.objects.create(author=request.user, group=group, text=text)
    return redirect('index')


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    profile_post_list = profile.posts.all()
    paginator = Paginator(profile_post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    user = request.user.username

    return render(request, 'profile.html', {"profile": profile, 'page': page, 'paginator': paginator, "user": user})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    author_post = author.posts.get(id=post_id)
    author_post_list = author.posts.all()
    paginator = Paginator(author_post_list, 5)
    user = request.user.username

    return render(request, 'post.html', {"author": author, 'author_post': author_post, 'paginator': paginator, "user": user})

@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    if author.username == request.user.username:
        post = get_object_or_404(Post, id=post_id)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                post.save()
                return redirect('post', username=username, post_id=post_id)

            return render(request, 'new_post.html', {"form": form})

        form = PostForm(instance=post)
        return render(request, 'new_post.html', {"form": form})

    return redirect('post', username=username, post_id=post_id)
