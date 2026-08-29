from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'api'

urlpatterns = [

    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/edit/<int:pk>/', UserEditView.as_view(), name='user-edit'),
    path('ticket/', TicketView.as_view(), name='ticket'),


]