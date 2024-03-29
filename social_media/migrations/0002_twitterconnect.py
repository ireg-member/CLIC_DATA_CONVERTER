# Generated by Django 4.2 on 2024-03-02 00:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterConnect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=512, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='twitter_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
