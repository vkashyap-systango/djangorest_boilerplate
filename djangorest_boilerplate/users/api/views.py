from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from .serializers import ImageSerializer,CategorySerializer
# from .models import Image, Category, Emoji
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
# Create your views here.

class IndexPageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def get(self, request):
        return Response()


class SocialLoginView(APIView):
    def get(self, request):
        from allauth.socialaccount.models import SocialToken
        user = request.user
        token = SocialToken.objects.filter(account__user=user, account__provider='facebook')
        if not token:
            token = SocialToken.objects.filter(account__user=user, account__provider='google')
        success = False
        if token:
            success = True
        return Response({'success':success})
