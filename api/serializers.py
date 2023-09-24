from rest_framework import serializers
from images.models import Image


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ImageListSerializer(serializers.ModelSerializer):
    original_link = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'upload_datetime', 'thumbnail', 'original_link')

    def get_original_link(self, obj):
        return obj.original_link


