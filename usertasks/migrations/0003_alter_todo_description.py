# Generated by Django 5.0.4 on 2024-05-20 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usertasks', '0002_remove_taskcompletion_is_done_post_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='description',
            field=models.TextField(max_length=255),
        ),
    ]