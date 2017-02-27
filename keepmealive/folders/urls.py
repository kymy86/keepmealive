from django.conf.urls import url, include
from folders.views import FolderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'folder', FolderViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]