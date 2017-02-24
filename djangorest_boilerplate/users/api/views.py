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


class FBLoginView(APIView):
    def get(self, request):
        import pdb; pdb.set_trace()
        return Response()
