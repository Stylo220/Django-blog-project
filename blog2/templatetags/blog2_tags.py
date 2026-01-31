from django import template
from ..models import Post, Comment
from django.db.models import Count, Q


register = template.Library()

@register.simple_tag()
def post_count():
    return Post.man_published.all().count()

@register.simple_tag()
def comment_count():
    return Comment.objects.filter(active=True).count()

@register.simple_tag()
def last_post():
    return Post.man_published.order_by('pb_date').last()


@register.inclusion_tag('partials/last_posts.html')
def last_posts(count = 3):
    l_posts = Post.man_published.order_by('-pb_date')[:count]
    return {'l_posts': l_posts}


# @register.inclusion_tag('partials/hot_posts.html')
# def hot_posts(count = 3):
#     posts = Post.man_published.all()
#     hot_posts = []
#     for post in posts:
#         comments = post.comments.filter(active=True).count()
#         hot_posts.append((post, comments))
#
#     sorted_hot_posts = sorted(hot_posts, key=lambda x: x[1], reverse=True)[:count]
#     final = []

@register.inclusion_tag('partials/hot_posts.html')
def hot_posts(count=3):
    posts = Post.man_published.annotate(
        comments_count=Count('comments', filter=Q(comments__active=True))
    ).order_by('-comments_count')[:count]
    return {'posts': posts}
