from folders.models import Folder
from folders.serializers import FolderSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class FolderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    queryset = Folder.objects.all()
    serializer_class = FolderSerializer