from rest_framework import serializers
from images.models import Image


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ImageListSerializer(serializers.ModelSerializer):
    original_link = serializers.SerializerMethodField()
    thumbnail_200px = serializers.URLField()
    thumbnail_400px = serializers.URLField()

    class Meta:
        model = Image
        fields = ('id', 'upload_datetime', 'thumbnail_200px', 'thumbnail_400px', 'original_link')

    def get_original_link(self, obj):
        return obj.original_link
