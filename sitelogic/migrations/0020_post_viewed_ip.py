# Generated by Django 4.1 on 2023-04-04 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitelogic', '0019_userip'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='viewed_ip',
            field=models.ManyToManyField(blank=True, related_name='viewed', to='sitelogic.userip'),
        ),
    ]
