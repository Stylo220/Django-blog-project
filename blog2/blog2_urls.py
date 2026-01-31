from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog2'

urlpatterns = [
    path('', views.index, name='index'),
    # path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<str:category>', views.post_list, name='post_list_category'),
    path('posts/detail/<int:id>', views.post_details, name='post_details'),
    path('ticket/', views.ticket, name='ticket'),
    path('post/<id>/comment', views.post_comment, name='post_comment'),
    path('post search/', views.post_search, name='post_search'),
    path('profile/', views.profile, name='profile'),
    path('profile/creating post/', views.creating_post, name='creating_post'),
    path('blog2/profile/deleting post/<id>', views.deleting_post, name='deleting_post'),
    path('blog2/profile/edit post/<id>', views.edit_post, name='edit_post'),
    path('blog2/profile/delete image/<id>', views.delete_image, name= 'delete_image'),

    #path('login/', views.user_login, name='user_login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='blog2:login'), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    #reset pass
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('blog2:password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('blog2:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #user_register
    path('register/', views.register, name='register'),
    path('profile/edit-profile', views.edit_profile, name='edit_profile'),
    path('profile/user-bio/', views.user_bio, name='user_bio'),



]
