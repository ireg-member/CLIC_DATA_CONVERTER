from django.contrib import admin
from social_media.models import FacebookPages, FacebookConnect, SocialAccountLinks, InstagramConnect

# Register your models here.

admin.site.register(FacebookPages)
admin.site.register(FacebookConnect)
admin.site.register(SocialAccountLinks)
admin.site.register(InstagramConnect)
