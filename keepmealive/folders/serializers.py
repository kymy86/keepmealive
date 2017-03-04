from rest_framework import serializers
from folders.models import Folder
from items.serializers import ItemSerializer

class FolderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    class Meta:
        model = Folder
        fields = ('id', 'name', 'isroot', 'idparent', 'created', 'items')
