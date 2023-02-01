from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post
from .forms import EmailPostForm

"""
def post_list(request):

    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range delver the last page
        posts = paginator.page(paginator.num_pages)

    return render(request, 'post_list.html', {'page':page,'posts':posts})

"""


class PostListView(ListView):

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post_list.html'


def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post, slug=post, 
                             status = 'published', 
                             publish__year=year,
                             publish__month = month,
                             publish__day = day)

    return render(request, 'post_detail.html', {'post':post})

def post_share(request, post_id):

    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post.url} {cd['name']}\'s comments:{cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']]) #replace 'admin@myblog.com' with your email account if you are using smtp
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'share.html', {'post':post, 'form':form, 'sent':sent})