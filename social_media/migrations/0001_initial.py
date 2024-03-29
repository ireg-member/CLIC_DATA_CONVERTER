# Generated by Django 5.0 on 2024-01-16 23:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookPages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_id', models.CharField(blank=True, max_length=256, null=True)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('category', models.CharField(blank=True, max_length=256, null=True)),
                ('page_token', models.CharField(blank=True, max_length=512, null=True)),
                ('page_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FacebookConnect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_user_id', models.CharField(blank=True, max_length=256, null=True)),
                ('fb_user_token', models.CharField(blank=True, max_length=512, null=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('fb_pages', models.ManyToManyField(blank=True, related_name='fb_pages', to='social_media.facebookpages')),
            ],
        ),
        migrations.CreateModel(
            name='InstagramConnect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram_id', models.CharField(blank=True, max_length=256, null=True)),
                ('access_token', models.CharField(blank=True, max_length=512, null=True)),
                ('instagram_account_name', models.CharField(blank=True, max_length=256, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SocialAccountLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook', models.BooleanField(default=False)),
                ('instagram', models.BooleanField(default=False)),
                ('twitter', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
