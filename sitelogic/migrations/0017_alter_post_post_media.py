# Generated by Django 4.1 on 2023-02-07 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitelogic', '0016_alter_post_post_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_media',
            field=models.ImageField(upload_to='%Y/%m/%d/', verbose_name='Превью'),
        ),
    ]
