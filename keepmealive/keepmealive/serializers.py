from rest_framework import serializers
from keepmealive.models import Folder

class FolderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    isroot = serializers.BooleanField(required=False, default=False)
    idparent = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data):
        return Folder.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.isroot = validated_data.get('isroot', instance.isroot)
        instance.idparent = validated_data.get('idparent', instance.isroot)
        instance.save()
        return instance

