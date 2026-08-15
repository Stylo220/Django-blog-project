from rest_framework import serializers
from blog2.models import *



class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'body', 'reading_time', 'category', 'author', 'pb_date', 'id']


class PostDetailCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['name', 'cm_body', 'created_at', 'id']


class PostDetailSerializer(serializers.ModelSerializer):
    comments = PostDetailCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'body', 'reading_time', 'category', 'author', 'pb_date', 'comments']




class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditAccount
        fields = ['bio', 'date_of_birth', 'user_photo', 'job']

class EditUserSerializer(serializers.ModelSerializer):
    editional = EditProfileSerializer(source='editaccount', read_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'editional', 'username']
        required_fields = ['email', 'username']
        read_only_fields = ['username']




class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'id']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['name', 'message', 'email', 'phone', 'subject']
