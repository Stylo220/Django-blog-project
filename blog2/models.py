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
        ('تکنولوژی','تکنولوژی'),
        ('هوش مصنوعی','هوش مصنوعی'),
        ('زبان برنامه نویسی','زبان برنامه نویسی'),
        ('سایر', 'سایر'),
    )

    title = models.CharField(max_length=250,verbose_name='عنوان')
    body = models.TextField(verbose_name='متن')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts', verbose_name='نویسنده')
    slug = models.SlugField(max_length=250, unique=True)
    pb_date = models.DateTimeField(default=datetime.now, verbose_name='تاریخ انتشار')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')
    status = models.CharField(max_length=2,choices= Status.choices , default=Status.DRAFT)
    reading_time = models.PositiveIntegerField(default=0, verbose_name='زمان مطالعه')
    category = models.CharField(max_length=30, choices = CATEGORY_CHOISES, default= 'سایر', verbose_name='دسته بندی')

    objects = models.Manager()
    man_published = PublishedManager()


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pb_date']
        indexes = [
            models.Index(fields=['-pb_date'])
        ]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

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
    name = models.CharField(max_length=250, verbose_name='اسم')
    message= models.TextField(verbose_name='پیام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    subject = models.CharField(verbose_name='عنوان پیام')
    time = models.DateTimeField(auto_now_add=True, verbose_name='زمان')

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return f"{self.name} - {self.subject}"



#comment-----------------------------------------------------------------------------------------------------

class Comment(models.Model):
    name = models.CharField(max_length=250, verbose_name= 'نام')
    cm_body = models.TextField(verbose_name= 'کامنت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ آپدیت')
    email = models.EmailField(verbose_name='ایمیل')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    active = models.BooleanField(default=False, verbose_name='تایید')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f"{self.name} - {self.post}"

#images-----------------------------------------------------------------------------------------------------

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images',verbose_name='پست')
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name='عنوان')
    created_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='post_img/', blank=True, null=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    def __str__(self):
        return self.title if self.title else 'None'

    def delete(self, *args, **kwargs):
        if self.img:
            self.img.delete(save=False)
        super().delete(*args, **kwargs)

#edit_account----------------------------------------------------------------------------------

class EditAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='editaccount')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')
    bio = models.TextField(max_length=400, blank=True, null=True, verbose_name='بیو')
    user_photo = models.ImageField(blank=True, null=True, verbose_name='تصویر پروفایل', upload_to='profile_photos/')
    job = models.CharField(max_length=100, blank=True, null=True, verbose_name='شغل')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'اکانت'
        verbose_name_plural = 'اکانت ها'





















