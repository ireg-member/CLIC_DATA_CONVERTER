from rest_framework import serializers
from social_media.models import SocialAccountLinks, FacebookConnect, FacebookPages


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccountLinks
        fields = '__all__'


class ConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookConnect
        fields = '__all__'


class FacebookPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookPages
        fields = '__all__'


class FacebookConnectSerializer(serializers.ModelSerializer):
    fb_pages = FacebookPagesSerializer(many=True)

    class Meta:
        model = FacebookConnect
        fields = '__all__'
