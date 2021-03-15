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
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            Post.objects.create(author=request.user, group=group, text=text)
            return redirect('index')

        return render(request, 'new_post.html', {"form": form})

    form = PostForm()
    return render(request, 'new_post.html', {"form": form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_post_list = author.posts.all()
    paginator = Paginator(author_post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    user = request.user.username

    return render(request, 'profile.html', {"author": author, 'page': page, 'paginator': paginator, "user": user})


def post_view(request, username, post_id):
    # тут тело функции
    author = get_object_or_404(User, username=username)
    author_post = author.posts.get(id=post_id)
    author_post_list = author.posts.all()
    paginator = Paginator(author_post_list, 5)
    user = request.user.username

    return render(request, 'post.html', {"author": author, 'author_post': author_post, 'paginator': paginator, "user": user})


def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    if author.username == request.user.username:
        post = get_object_or_404(Post, id=post_id)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                post.save()
                return redirect('index')

            return render(request, 'new_post.html', {"form": form})
        form = PostForm(instance=post)
        return render(request, 'new_post.html', {"form": form})
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)
    return redirect('index')