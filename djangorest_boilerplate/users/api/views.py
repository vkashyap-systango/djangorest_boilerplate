from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from .serializers import ImageSerializer,CategorySerializer
# from .models import Image, Category, Emoji
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.contrib.sites.models import Site
from djangorest_boilerplate.lib.authentication import CsrfExemptSessionAuthentication
from django.template import RequestContext
from django.shortcuts import render_to_response
from .serializers import LoginSerializer, PasswordResetSerializer, ConfirmPasswordResetSerializer, BaseUserSerializer
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from djangorest_boilerplate.lib.util import send_password_reset_email
from users.models import BaseUser


class IndexPageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'
    def get(self, request):
        return Response({'request':request})

class SignUp(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = BaseUserSerializer

    def post(self, request, *args, **kwargs):
        print("initial_data: ",request.data)
        return self.create(request, *args, **kwargs)

class SocialLoginView(APIView):

    def get(self, request):
        from allauth.socialaccount.models import SocialToken
        user = request.user
        success = False
        if user:
            success = True
        return Response({'success':success, 'user':{'email':user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'id':user.id}})

    def post(self, request):
        return Response()

class LoginView(APIView):

    serializer_class = LoginSerializer
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            # Create session in db
            auth_login(request, user)
            registration_id = serializer.initial_data.get('registration_id')
            request.session['registration_id'] = registration_id
            response_data = {'success': 'User session created successfully.','first_name':user.first_name,'last_name':user.last_name,'id':user.id}
            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    permission_classes = ()
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, *args, **kwargs):
        registration_id = request.session._session_cache.get('registration_id')
        user = request.user
        logout(request)
        return Response({'status': True, 'msg': 'Successfully logged out'})

class ResetPassword(APIView): 
    serializer_class = PasswordResetSerializer
    permission_classes = ()
    authentication_classes = ()
   
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user')
            token = default_token_generator.make_token(user)
            send_password_reset_email.delay('http://localhost:8000/api/users/password/reset/confirm/'+token+'/', [user.email,])
            return Response({"success":"true"})
        return Response({"success":"false","reset_token":token})


class ConfirmPasswordReset(APIView):
    serializer_class = ConfirmPasswordResetSerializer
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        token = kwargs.get('password_reset_token')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = BaseUser.objects.get(id=request.data.get("u_id"))

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(serializer.validated_data.get("new_password"))
                user.save()
                return  Response({"success":"password saved"})
            return Response({"success":"true"})
        return Response({"success":"false"})

