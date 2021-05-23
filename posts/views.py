from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from posts.models import Post, RecentPosts
from posts.forms import PostForm


def index(request):
    # RecentPosts is a proxy model, see posts/models.py
    posts = RecentPosts.objects.all()
    query = request.GET.get('q') # q -> query
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'posts': posts}
    return render(request, 'posts/index.html', context)


def post_detail(request, id):
    # context = {'post': Post.objects.get(id=id)} # without handling 404
    context = {'post': get_object_or_404(Post, id=id)}
    return render(request, 'posts/detail.html', context)


@login_required(login_url='/login/')
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            post = form.save()
            messages.success(request, 'You just created a post')
            # return HttpResponseRedirect(reverse('detail', args=[post.id])) -> another way
            return HttpResponseRedirect(post.get_absolute_url())
    return render(request, 'posts/create.html', context)


@login_required(login_url='/login/')
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'You just deleted the post')
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/login/')
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            post = form.save()
            messages.success(request, 'You just updated the post')
            # return HttpResponseRedirect(reverse('detail', args=[post.id])) -> another way
            return HttpResponseRedirect(post.get_absolute_url())
    return render(request, 'posts/create.html', context)
