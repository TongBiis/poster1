from captcha.fields import CaptchaField
from ckeditor.widgets import CKEditorWidget
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError

from .models import Post, Comment, CommentReply


class PostForm(forms.ModelForm):
    # post_content = forms.CharField(widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'категория не выбрана'

    captcha = CaptchaField()

    class Meta:
        model = Post
        fields = ['post_title', 'post_content', 'cat']

    def clean_post_title(self):
        post_title = self.cleaned_data['post_title']
        if len(post_title) >= 250:
            raise ValidationError('Длина превышает 250 символов')

        return post_title


class CommentPostForm(forms.ModelForm):
    # captcha = CaptchaField()

    widget = {
        'post_comment': forms.HiddenInput(),
    }

    class Meta:
        widgets = {
            'comment_content': forms.Textarea(attrs={'class': 'ta', 'cols': 15, 'rows': 5}),
        }
        model = Comment
        fields = ['comment_content']


class CommentReplyForm(forms.ModelForm):
    # captcha = CaptchaField()

    class Meta:
        model = CommentReply
        fields = ['reply_content', 'parent_comment']
