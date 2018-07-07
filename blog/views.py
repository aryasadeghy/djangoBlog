from django.shortcuts import render,get_object_or_404
# from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

from .forms import EmailPostForm, CommentForm
from blog.models import Post,Comment

# Create your views here.

def post_list(request, tag_slug=None):
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    tag=None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])


    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts =  paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page':page,'posts': posts, 'tags':tag})

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)

            new_comment.post = post

            new_comment.save()
    else:
        comment_form =CommentForm()
    
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts =  Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,'blog/post/detail.html', {'post': post,
                                                    'comments': comments,
                                                    'similar_posts': similar_posts,
                                                    'comment_form': comment_form})
    




def post_share(request, pk):

    post = get_object_or_404(Post, pk=pk)
    print(post)
    sent = False

    if request.method == 'POST':

        form = EmailPostForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommonds you reading "{}"'.format(cd['name'], cd['email'], post_url)
            message = 'Read {} at {}   comments: {}'.format(post.title, post_url,cd['comments'])
            send_mail(subject,message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post,
                                                    'sent':sent,
                                                    'form': form})     