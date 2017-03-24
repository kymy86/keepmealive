"""keepmealive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from keepmealive.views import PasswordRecoveryAPIView, PasswordResetAPIView, UserApiView


urlpatterns = [
    url(r'^api/users/$', UserApiView.as_view(), name='users'),
    url(r'^api/users/forgot/$', PasswordRecoveryAPIView.as_view(), name='forgot_password'),
    url(r'^api/users/reset/$', PasswordResetAPIView.as_view(), name='reset_password'),
    url(r'^api/folders/', include('folders.urls')),
    url(r'^api/items/', include('items.urls')),
    url(r'^api/auth/token/', obtain_jwt_token),
    url(r'^api/refresh/token/', refresh_jwt_token),
    url(r'^api/verify/token/', verify_jwt_token),
]

