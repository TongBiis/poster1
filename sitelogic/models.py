from time import time

import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
# from django.utils.text import slugify
from django.utils import timezone
from transliterate import slugify
from ckeditor.fields import RichTextField
from timezone_field import TimeZoneField


def gen_slug(string):
    finally_slug = slugify(string, language_code="ru")
    return finally_slug + '-'


class Post(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    post_title = models.CharField(max_length=250, verbose_name='Заголовок')
    post_slug = models.SlugField(max_length=250, unique=True, verbose_name='URL', null=True, blank=True)
    post_content = RichTextUploadingField(max_length=450000, verbose_name='Содержание', default='test')
    post_time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    post_time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    # post_media = models.ImageField(upload_to='%Y/%m/%d/', verbose_name='Превью')
    cat = models.ForeignKey('PostCategory', on_delete=models.PROTECT, null=True, verbose_name='Форум')
    views_count = models.IntegerField(default=0)
    viewed_ip = models.ManyToManyField('UserIp', related_name='viewed', blank=True)
    vvv = models.CharField(max_length=50, verbose_name='Просмотревшие IP', blank=True)

    def get_utc_time(self):
        return self.post_time_create.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    def save(self, *args, **kwargs):
        self.post_slug = gen_slug(self.post_title + str(int(self.uuid)))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse('show_post',
                       kwargs={'post_title_slug': self.post_slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

        ordering = ['post_title', 'post_content']


class Comment(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    comment_content = models.CharField(max_length=50000)
    comment_create = models.DateTimeField(auto_now_add=True, null=True)
    post_comment = models.ForeignKey(Post, related_name='post_comments', blank=True, on_delete=models.CASCADE,
                                     null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def get_replies(self):
        return CommentReply.objects.filter(parent_comment=self)

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ["-comment_create"]
        verbose_name = "Комментарий"
        verbose_name_plural = 'Комментарии'


class CommentReply(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    parent_comment = models.ForeignKey(Comment, related_name='par_com', on_delete=models.CASCADE, blank=True, null=True)
    reply_content = models.TextField()

    def get_parent_comment(self):
        return CommentReply.objects.filter(parent_comment=Comment)


class PostCategory(models.Model):
    category_name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

        ordering = ['pk']

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('cat_posts', kwargs={'cat_slug': self.slug})


class UserIp(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    IP = models.CharField(max_length=50)

    def __str__(self):
        return self.IP

# class SKEditor(models.Model):
#     ckeditor_test = CKEditor5Field('Text', config_name='extends')

# class Commentaries(models.Model):
#     comment_nickname = models.CharField(max_length=30, defaul="Anonymous")
#     comment_content = models.TextField(max_length=1000000)
#     comment_created = models.DateTimeField(auto_now_add=True)
#     comment_active = models.BooleanField(default=True)

# class Hit(models.Model):
#     url = models.CharField(max_length=1000, unique=True)
#     count = models.PositiveIntegerField(default=0)
