from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
# from taggit.models import 



def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts_list')
    else:
        form = PostForm()
    return render(request, 'blog/post/post_create.html', {'form': form})


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts' : posts, 'page':page})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug= post, 
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    comments = post.comments.all()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            obj = Comment()
            obj.body = comment_form.cleaned_data['body']
            obj.author = request.user
            obj.post = post
            obj.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post':post, 
                                                    'comments':comments, 
                                                    'new_comment': new_comment, 
                                                    'comment_form': comment_form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.updated_at = timezone.now()
            post.save()
            return redirect('posts_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post/post_edit.html', {'form': form})
    

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('posts_list')
    return render(request, 'blog/post/post_delete.html', {'post':post})

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = get_object_or_404(Post, pk=comment.post.pk)
    if request.method == "POST":
        comment.delete()
        return redirect(post.get_absolute_url())
    return render(request, 'blog/post/delete_comment.html', {'comment':comment, 'post': post})