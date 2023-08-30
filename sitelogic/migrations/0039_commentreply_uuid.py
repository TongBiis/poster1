# Generated by Django 4.1 on 2023-05-10 13:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sitelogic', '0038_alter_comment_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentreply',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]