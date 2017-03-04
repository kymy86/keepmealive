from django.conf.urls import url, include
from items.views import ItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'item', ItemViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]