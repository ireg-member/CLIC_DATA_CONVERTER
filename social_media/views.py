import requests
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet

from social_media.models import FacebookConnect, FacebookPages, InstagramConnect, SocialAccountLinks
from social_media.serializers import ConnectSerializer, FacebookConnectSerializer, SocialLinkSerializer


class FacebookConnectViewset(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        user_token = self.request.query_params.get('user_token', None)
        fb_access_token = self.request.query_params.get('access_token', None)
        fb_user_id = self.request.query_params.get('fb_user_id', None)
        if fb_user_id and user_token and fb_access_token:
            token = Token.objects.get(key=user_token)
            user = token.user
            endpoint = f"https://graph.facebook.com/{fb_user_id}/accounts?access_token={fb_access_token}"
            reqeust = requests.get(endpoint)
            pages_ids = []
            if reqeust.status_code == 200:
                facebook_connect = FacebookConnect.objects.filter(user=user).first()
                if facebook_connect:
                    facebook_connect.fb_pages.all().delete()
                    facebook_connect.delete()
                user_data = reqeust.json()
                for data in user_data['data']:
                    facebook_page = FacebookPages.objects.create(name=data['name'], page_id=data['id'],
                                                                 page_token=data['access_token'],
                                                                 category=data['category'])
                    pages_ids.append(facebook_page.id)
                fb_connects = FacebookConnect.objects.create(user=user, fb_user_id=fb_user_id,
                                                             fb_user_token=fb_access_token, status=True)
                fb_connects.fb_pages.add(*pages_ids)
                fb_connects.save()
                facebook_link, created = SocialAccountLinks.objects.get_or_create(user=user)
                facebook_link.facebook = True
                facebook_link.save()
                fb_connects_data = FacebookConnectSerializer(fb_connects).data
                return Response(fb_connects_data, status=status.HTTP_200_OK)
            else:
                return Response(reqeust.json(), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Please add these query params: 'user_token', 'access_token', 'fb_user_id'",
                            status=status.HTTP_200_OK)

    def delete(self, reqeust, *args, **kwargs):
        if reqeust.user:
            facebook_connect = FacebookConnect.objects.get(user=reqeust.user)
            facebook_connect.fb_pages.all().delete()
            facebook_connect.delete()
            facebook_link = SocialAccountLinks.objects.filter(user=reqeust.user).first()
            facebook_link.facebook = False
            facebook_link.save()
            return Response({"msg": "Your facebook link account has been removed"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Please add user token"}, status=status.HTTP_400_BAD_REQUEST)


class InstagramConnectViewset(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        user_token = self.request.query_params.get('user_token', None)
        fb_access_token = self.request.query_params.get('access_token', None)
        fb_user_id = self.request.query_params.get('fb_user_id', None)
        if fb_user_id and user_token and fb_access_token:
            token = Token.objects.get(key=user_token)
            user = token.user
            endpoint = f"https://graph.facebook.com/{fb_user_id}/accounts?fields=instagram_business_account,id,name&access_token={fb_access_token}"
            reqeust = requests.get(endpoint)
            account_title = None
            if reqeust.status_code == 200:
                InstagramConnect.objects.filter(user=user).delete()
                for insta_id in reqeust.json()['data']:
                    business_id = insta_id.get('instagram_business_account', None)
                    if business_id:
                        if account_title is None:
                            account_title = insta_id['name']
                        else:
                            account_title += f", {insta_id['name']}"
                        InstagramConnect.objects.create(user=user, instagram_id=business_id['id'],
                                                        access_token=fb_access_token,
                                                        instagram_account_name=insta_id['name'])
                        facebook_link, created = SocialAccountLinks.objects.get_or_create(user=user)
                        facebook_link.instagram = True
                        facebook_link.save()
            insta_user = InstagramConnect.objects.filter(user=user)
            if not insta_user:
                return Response({"msg": "Please connect your business account."}, status=status.HTTP_200_OK)
            account = "account"
            if account_title:
                if len(account_title.split(',')) > 1:
                    account = "accounts"
            else:
                return Response({"msg": "Please connect your business account."}, status=status.HTTP_200_OK)
            return Response(
                {"msg": f"Your instagram {account} '{account_title}' has been successfully linked the ONIT Athlete."},
                status=status.HTTP_200_OK)

    def delete(self, reqeust, *args, **kwargs):
        if reqeust.user:
            InstagramConnect.objects.filter(user=reqeust.user).delete()
            facebook_link = SocialAccountLinks.objects.filter(user=reqeust.user).first()
            facebook_link.instagram = False
            facebook_link.save()
            return Response({"msg": "Your Instagram link account has been removed"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Please add user token"}, status=status.HTTP_400_BAD_REQUEST)


class UploadPostOnFacebook(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        title = self.request.query_params.get('title')
        thumbnail = self.request.query_params.get('thumbnail')
        fb_connect = FacebookConnect.objects.filter(user=self.request.user).first()
        fb_connect_data = ConnectSerializer(fb_connect).data
        if fb_connect_data['fb_pages']:
            fb_pages = FacebookPages.objects.filter(id__in=fb_connect_data['fb_pages'])
            upload_image = None
            for page in fb_pages:
                endpoint = f"https://graph.facebook.com/{page.page_id}/photos"
                json_data = {
                    "access_token": page.page_token,
                    "url": thumbnail,
                    "message": title
                }
                upload_image = requests.post(endpoint, json=json_data)
            if upload_image.status_code == 200:
                return Response(upload_image.json(), status=upload_image.status_code)
            elif upload_image.status_code == 190:
                return Response({"msg": "Your session has been expired, please reconnect your Facebook account"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(upload_image.json(), status=upload_image.status_code)
        else:
            return Response({'msg': 'You don"t have connect any facebook page. Please connect facebook page first.'},
                            status=status.HTTP_400_BAD_REQUEST)


class UploadPostOnInstagram(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, reqeust, *args, **kwargs):
        title = self.request.query_params.get('title')
        thumbnail = self.request.query_params.get('thumbnail')
        insta_connect = InstagramConnect.objects.filter(user=self.request.user)
        for insta_id in insta_connect:
            endpoint = f"https://graph.facebook.com/{insta_id.instagram_id}/media"
            json_data = {
                "access_token": insta_id.access_token,
                "caption": title,
                "image_url": thumbnail
            }
            upload_image = requests.post(endpoint, json=json_data)
            if upload_image.status_code == 200:
                publish_endpoint = f'https://graph.facebook.com/{insta_id.instagram_id}/media_publish?creation_id={upload_image.json()["id"]}'
                publish_image = requests.post(publish_endpoint, json=json_data)
                if publish_image.status_code == 200:
                    return Response(publish_image.json(), status=upload_image.status_code)
                else:
                    return Response(upload_image.json(), status=upload_image.status_code)
            else:
                return Response(upload_image.json(), status=upload_image.status_code)
        else:
            return Response(
                {'msg': 'You don"t have connect any Instagram account. Please connect Instagram account first.'},
                status=status.HTTP_400_BAD_REQUEST)


class UserSocialLinks(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SocialLinkSerializer
    queryset = SocialAccountLinks.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
