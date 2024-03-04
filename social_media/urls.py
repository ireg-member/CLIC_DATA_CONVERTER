from django.urls import path, include

from social_media.views import FacebookConnectViewset, InstagramConnectViewset, UploadPostOnFacebook, \
    UploadPostOnInstagram, UserSocialLinks, UploadTweetView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register("social_account_list", UserSocialLinks, basename="social_account_list")

urlpatterns = [
    path("", include(router.urls)),
    path('facebook_connect/', FacebookConnectViewset.as_view(), name='facebook_connect'),
    path('instagram_connect/', InstagramConnectViewset.as_view(), name='instagram_connect'),
    path('upload_post_on_fb/', UploadPostOnFacebook.as_view(), name='upload_post_on_fb'),
    path('upload_post_on_insta/', UploadPostOnInstagram.as_view(), name='upload_post_on_insta'),
    path('upload_tweets/', UploadTweetView.as_view(), name='upload_tweets'),
]
