# Generated by Django 4.1 on 2023-01-27 13:59

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitelogic', '0014_alter_post_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='test', max_length=450000, verbose_name='Содержание'),
        ),
    ]