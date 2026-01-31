from email.policy import default

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import forbid_multi_line_headers
from django.template.context_processors import request

from .models import Ticket, Comment, Post, PostImage, User, EditAccount
from django import forms

#ticket------------------------------------------------------------------------------------------------

class TicketForm(forms.Form):

    SUB_CHOISES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )

    name = forms.CharField(max_length=250, label='نام', required=True)
    message = forms.CharField(widget=forms.Textarea, label='پیام', required=True)
    email = forms.EmailField(required=True, label='ایمیل')
    phone = forms.CharField(label='شماره تماس', max_length=11, required=False, min_length=11)
    subject = forms.ChoiceField(choices = SUB_CHOISES,label='یک مورد را انتخاب کنید' ,initial = 'پیشنهاد')

#comment------------------------------------------------------------------------------------------------

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'cm_body', 'email']

#search--------------------------------------------------------------------------------------------------

class PostSearch(forms.Form):
    query = forms.CharField(required=True)


#creating_post---------------------------------------------------------------------------------------------------------

class CreatingPostForm(forms.ModelForm):
    img1 = forms.ImageField(label='تصویر اول', required=True)
    img2 = forms.ImageField(label='تصویر دوم', required=False)
    class Meta:
        model = Post
        fields = ['title', 'body', 'reading_time', 'category']

#login form------------------------------------------------------------------------------------------------

# class UserLogin(forms.Form):
#     username = forms.CharField(max_length=250, required=True)
#     password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)



#user_register----------------------------------------------------------------------------------------------------

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='password')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label='password confirm')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email' )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords are Not the same!')
        return cd['password2']

#edit_profile---------------------------------------------------------------------------------------------

class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class EditAccountForm(forms.ModelForm):

    class Meta:
        model = EditAccount
        fields = ('date_of_birth', 'bio', 'user_photo', 'job')







