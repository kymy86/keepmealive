from keepmealive.serializers import UserSerializer, PasswordResetSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from keepmealive.models import PasswordForgotRequest
from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError

class UserApiView(APIView):
    permission_classes = (IsAuthenticated, )
    throttle_classes = (UserRateThrottle, )

    queryset = User.objects.all()

    def get(self, request):
        """
        Return user properties only if requester
        has a super-admin role, otherwise 404 is raised
        If id is equal to 'me', the properties of the
        current user is returned.
        """
        user = request.query_params.get('user', None)
        if user is None:
            raise Http404

        if user == 'me':
            serializer = UserSerializer(request.user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Create a new user (administrator only can perform this operation)
        """
        if not request.user.is_superuser:
            return Response('{You\'re not allowed to perform this operation}', status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.create_user(
                username=serializer.data['username'],
                email=serializer.data['email'],
                password=serializer.data['password'])
            user.last_name=serializer.data['last_name']
            user.first_name=serializer.data['first_name']
            user.save()
        except IntegrityError as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_201_CREATED)

class PasswordRecoveryAPIView(APIView):
    permission_classes = (AllowAny, )
    throttle_classes = (AnonRateThrottle, )

    queryset = User.objects.all()

    """ send recovery email if the username exists """
    def get(self, request):
        # if username isn't in the get request, raise a 404 error
        username = request.query_params.get('username', None)
        if username is None:
            raise Http404
        user = get_object_or_404(self.queryset, username=username)
        #create new password request
        preq = PasswordForgotRequest(user=user, ip_addr=request.META['REMOTE_ADDR'])
        preq.save()

        #send recovery email
        subject = "Keepmealive - Recovery password message"
        link = "/recover/password/?hash="+preq.uuid_str
        html_message = "Click on this link <a href='{link}'>{link}</a> to start the password recovery procedure".format(
            link=link
        )
        send_mail(
            subject,
            message="Password recovery email",
            html_message=html_message,
            from_email=settings.FROM_EMAIL,
            recipient_list=(user.email, ),
            fail_silently=True
        )

        return Response(status=status.HTTP_202_ACCEPTED)

class PasswordResetAPIView(APIView):
    permission_classes = (AllowAny, )
    throttle_classes = (AnonRateThrottle, )

    """ update user password if the give hash is valid """
    def post(self, request):
        #hash, password and email fields must exists in the request body
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uuid = serializer.data['hash']
        pwdreq = get_object_or_404(PasswordForgotRequest, hash=uuid, used=0)
        if pwdreq.user.email != serializer.data['email']:
            return Response(
                {"you're not authorized to perform this operation"},
                status=status.HTTP_403_FORBIDDEN)
        #update password request record
        pwdreq.used = True
        pwdreq.save()
        # update password
        user = User.objects.get(pk=pwdreq.user.pk)
        user.set_password(serializer.data['password'])
        user.save()

        return Response(status=status.HTTP_200_OK)

