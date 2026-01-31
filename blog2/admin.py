from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
import jdatetime
from django.utils import timezone
from .models import Post, Ticket, Comment, PostImage, EditAccount
from .views import ticket


# admin inlines

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class ImageInline(admin.TabularInline):
    model = PostImage
    extra = 0
#------------------------------------------------------------------------------------

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'pb_date', 'status', 'category']
    list_filter = (('pb_date', JDateFieldListFilter), 'status', 'author', 'category')
    ordering = ['-pb_date']
    search_fields = ['body', 'title', 'author__username']
    raw_id_fields = ['author']
    date_hierarchy = 'pb_date'
    prepopulated_fields = {'slug': ['title']}
    list_editable = ['status','category']
    list_display_links = ['title', 'author']
    inlines = ImageInline, CommentInline


@admin.register(Ticket)
class ticketAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'time']
    list_filter = [('time', JDateFieldListFilter), 'subject']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at','post' , 'active']
    list_filter = [('created_at', JDateFieldListFilter), 'active']
    search_fields = ['name', 'email', 'cm_body']
    list_editable = ['active']


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title']


@admin.register(EditAccount)
class EditAccountAdmin(admin.ModelAdmin):
    list_display = ['date_of_birth', 'bio', 'user_photo', 'job']