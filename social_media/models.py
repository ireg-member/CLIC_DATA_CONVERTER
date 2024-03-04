from django.db import models


class FacebookPages(models.Model):
    page_id = models.CharField(max_length=256, null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    category = models.CharField(max_length=256, null=True, blank=True)
    page_token = models.CharField(max_length=512, null=True, blank=True)
    page_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class FacebookConnect(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)
    fb_user_id = models.CharField(max_length=256, null=True, blank=True)
    fb_user_token = models.CharField(max_length=512, null=True, blank=True)
    status = models.BooleanField(default=False)
    fb_pages = models.ManyToManyField('FacebookPages', related_name='fb_pages', blank=True)


class SocialAccountLinks(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)
    facebook = models.BooleanField(default=False)
    instagram = models.BooleanField(default=False)
    twitter = models.BooleanField(default=False)


class InstagramConnect(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)
    instagram_id = models.CharField(max_length=256, null=True, blank=True)
    access_token = models.CharField(max_length=512, null=True, blank=True)
    instagram_account_name = models.CharField(max_length=256, null=True, blank=True)


class TwitterConnect(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='twitter_user')
    token = models.CharField(max_length=512, null=True, blank=True)
