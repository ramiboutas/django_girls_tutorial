from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from posts.models import Post, RecentOrderedPost
from posts.forms import PostForm


def index(request):
    context = {'posts': RecentOrderedPost.objects.all()} # RecentOrderedPost is a proxy model, see posts/models.py
    return render(request, 'posts/index.html', context)


def post_detail(request, id):
    # context = {'post': Post.objects.get(id=id)} # without handling 404
    context = {'post': get_object_or_404(Post, id=id)}
    return render(request, 'posts/detail.html', context)

@login_required(login_url='/')
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            post = form.save()
            # return HttpResponseRedirect(reverse('detail', args=[post.id])) -> another way
            return HttpResponseRedirect(post.get_absolute_url())
    return render(request, 'posts/create.html', context)

@login_required(login_url='/')
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
    return HttpResponseRedirect(reverse('index'))
