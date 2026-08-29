from tkinter.constants import CASCADE
from datetime import datetime
from django.contrib.auth.models import User
from django.core.files.storage import storages
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


# Create your models here.

#Post----------------------------------------------------------------------------------------------------------

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DR', 'draft'
        PUBLISHED = 'PB', 'published'
        REJECTED =  'RJ', 'rejected'

    CATEGORY_CHOISES = (
        ('technology','technology'),
        ('ai','ai'),
        ('programming language','programming language'),
        ('other', 'other'),
    )

    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts')
    slug = models.SlugField(max_length=250, unique=True)
    pb_date = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices= Status.choices , default=Status.DRAFT)
    reading_time = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=30, choices = CATEGORY_CHOISES, default= 'other', )

    objects = models.Manager()
    man_published = PublishedManager()


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pb_date']
        indexes = [
            models.Index(fields=['-pb_date'])
        ]


    def get_absolute_url(self):
        return reverse('blog2:post_details', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        p_images = self.images.all()
        for img in p_images:
            if img.img:
                storage, path = img.img.storage, img.img.path
                storage.delete(path)
        super().delete(*args, **kwargs)


#Ticket-----------------------------------------------------------------------------------------------------

class Ticket(models.Model):
    name = models.CharField(max_length=250)
    message= models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    subject = models.CharField()
    time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} - {self.subject}"



#comment-----------------------------------------------------------------------------------------------------

class Comment(models.Model):
    name = models.CharField(max_length=250)
    cm_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    def __str__(self):
        return f"{self.name} - {self.post}"

#images-----------------------------------------------------------------------------------------------------

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='post_img/', blank=True, null=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    def __str__(self):
        return self.title if self.title else 'None'

    def delete(self, *args, **kwargs):
        if self.img:
            self.img.delete(save=False)
        super().delete(*args, **kwargs)

#edit_account----------------------------------------------------------------------------------

class EditAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='editaccount')
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=400, blank=True, null=True)
    user_photo = models.ImageField(blank=True, null=True, upload_to='profile_photos/')
    job = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username




















