# Generated by Django 5.1.3 on 2024-11-20 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hashtag', '0001_initial'),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='hashtags',
            field=models.ManyToManyField(blank=True, related_name='tweets', to='hashtag.hashtag'),
        ),
    ]