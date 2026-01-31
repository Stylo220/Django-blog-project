from django.contrib.admin.templatetags.admin_list import pagination
from django.contrib.auth.password_validation import password_changed
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog2.models import Post, Ticket, Comment, PostImage, EditAccount, User
from django.views.generic import ListView, DetailView
from .forms import TicketForm, CommentForm, PostSearch, CreatingPostForm, UserRegisterForm, EditAccount, EditUserForm, \
    EditAccountForm
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q, Value, Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from random import *
# Create your views here.

def index(request):
    posts = Post.man_published.all()
    post = choice(posts)

    return render(request, 'blog/index.html', {'post':post})

def post_list(request, category=None):

    if category is not None:
        posts = Post.man_published.filter(category=category)
    else:
        posts = Post.man_published.all().order_by('-pb_date')

    paginator = Paginator(posts,5)
    page_num = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_num)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    context = {
        'posts':posts,
        'category':category,
    }
    return render(request, 'blog/post_list.html', context)

# class PostListView(ListView):
#     queryset = Post.man_published.all()
#     context_object_name = 'posts'
#     paginate_by = 5
#     template_name = 'blog/post_list.html'

def post_details(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    form = CommentForm()
    comments = post.comments.filter(active=True)

    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }

    return render(request, 'blog/post_details.html', context)

# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post_details.html'


def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj = Ticket.objects.create(
                name = cd['name'],
                message = cd['message'],
                email = cd['email'],
                phone = cd['phone'],
                subject = cd['subject'],
            )
            return redirect('blog2:ticket')
    else:
        form = TicketForm()

    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def post_comment(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(request, 'forms/comment submit page.html', context)


def post_search(request):
    query = None
    resaults = []
    if 'query' in request.GET:
        form = PostSearch(data = request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            resault1 = Post.man_published.annotate(similarity = TrigramSimilarity('title', query)).filter(similarity__gt=0.1)
            resault2 = Post.man_published.annotate(similarity = TrigramSimilarity('body', query)).filter(similarity__gt=0.01)
            resault3 = Post.man_published.filter(author__username__icontains=query).annotate(similarity = Value(0))
            resaults = (resault1 | resault2 | resault3).order_by('-similarity')
    context = {
        'query': query,
        'resaults': resaults,
    }
    return render(request, 'blog/search_field.html', context)


#create post--------------------------------------------------------------------------------------------
@login_required
def creating_post(request):
    if request.method == 'POST':
        form = CreatingPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit= False)
            post.author = request.user
            post.status = Post.Status.DRAFT
            post.save()
            if form.cleaned_data.get('img1'):
                PostImage.objects.create(img=form.cleaned_data['img1'], post=post)

            if form.cleaned_data.get('img2'):
                PostImage.objects.create(img=form.cleaned_data['img2'], post=post)
            return redirect('blog2:profile')
    else:
        form = CreatingPostForm()
    return render(request, 'forms/creating-post.html', {'form': form})


#profile-------------------------------------------------------------------------------------------------
@login_required
def profile(request):
    user = request.user
    posts = Post.man_published.filter(author=user)
    cm_posts = (
            posts
            .annotate(active_comments_count=Count('comments', filter=Q(comments__active=True)))
            .filter(active_comments_count__gt=0)
    )
    draft_p = Post.objects.filter(status = Post.Status.DRAFT, author = user)
    rejected_p = Post.objects.filter(status = Post.Status.REJECTED, author = user)

    paginator = Paginator(posts, 3)
    page_num = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_num)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)



    context = {
        'cm_posts':cm_posts,
        'draft_p':draft_p,
        'rejected_p':rejected_p,
        'user':user,
        'posts':posts,
    }

    return render(request, 'blog/profile.html', context)


#deleting post------------------------------------------------------------------------------------
@login_required
def deleting_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog2:profile')
    else:
        return render(request, 'forms/deleting-post.html', {'post':post})


#edit post----------------------------------------------------------------------------------------
@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id = id)
    if request.method == 'POST':
        form = CreatingPostForm(request.POST, request.FILES, instance= post)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.status = Post.Status.DRAFT
            post.save()
            PostImage.objects.create(img = form.cleaned_data['img1'], post = post)
            PostImage.objects.create(img=form.cleaned_data['img2'], post=post)
            return redirect('blog2:profile')
    else:
        form = CreatingPostForm(instance= post)

    context = {
        'form': form,
        'post': post,

    }

    return render(request, 'forms/creating-post.html', context)

#delete post image in profile-------------------------------------------------------------------------------
@login_required
def delete_image(request, id):
    image = get_object_or_404(PostImage, id=id)
    post_id = image.post.id
    post = image.post
    if post.images.filter(img__isnull=False).count() > 1:
        image.delete()
    else:
        return HttpResponseForbidden('یک تصویر حتما باید باشد!')
    return redirect('blog2:edit_post', id= post_id)


#user login---------------------------------------------------------------------------------------------------

# def user_login(request):
#     if request.method == 'POST':
#         form = UserLogin(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('blog2:profile')
#                 else:
#                     return HttpResponse('You are Not active! contact admin')
#             else:
#                 return HttpResponse('Invalid account! register first...')
#     else:
#         form = UserLogin()
#     return render(request, 'forms/user-login.html', {'form':form})

#user_register-----------------------------------------------------------------------------------------------

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            EditAccount.objects.create(user = user)
            return render(request, 'registration/register_done.html', {'user':user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form':form})

#edit_user_prifile-------------------------------------------------------------------------------------------

@login_required
def edit_profile(request):
    if request.method == 'POST':
        edit_user_form = EditUserForm(request.POST, instance = request.user)
        edit_account_form = EditAccountForm(request.POST, files = request.FILES, instance = request.user.editaccount)
        if edit_user_form.is_valid() and edit_account_form.is_valid():
            edit_account_form.save()
            edit_user_form.save()
            return redirect('blog2:profile')
    else:
        edit_user_form = EditUserForm(instance = request.user)
        edit_account_form = EditAccountForm(instance=request.user.editaccount)

    context = {
        'edit_user_form': edit_user_form,
        'edit_account_form': edit_account_form
    }
    return render(request, 'registration/edit_account.html', context)

#user_bio---------------------------------------------------------------------------------------------

def user_bio(request):
    user = request.user
    account = user.editaccount
    context = {
        'user':user,
        'account':account,
    }
    return render(request, 'blog/user_bio.html', context)












