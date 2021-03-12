from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Group, User
from .forms import PostForm
from django.contrib.auth.decorators import login_required

def index(request):
    latest = Post.objects.order_by('-pub_date')[:11]
    
    return render(request, 'index.html', {'posts': latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    
    return render(request, "group.html", {"group": group, "posts": posts})

@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group'] 
            Post.objects.create(author=request.user , group=group, text=text)
            return redirect ('index')

        return render(request, 'new_post.html', {"form": form})

    form = PostForm()
    return render(request, 'new_post.html', {"form": form})
