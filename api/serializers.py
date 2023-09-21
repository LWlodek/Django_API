from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
    tier = serializers.CharField(required=False)  # Make the tier field optional