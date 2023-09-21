from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ImageUploadSerializer
from images.models import Image, Tier


# Assuming you have a default tier named 'Basic' in your Tier model
default_tier, created = Tier.objects.get_or_create(name='Basic')

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_image = serializer.validated_data['image']
            # image_instance = Image.objects.create(user=request.user, image_file=uploaded_image)

            # Create an Image instance with the default tier
            image_instance = Image.objects.create(
                user=request.user,  # Assuming user is authenticated
                image_file=uploaded_image,
                tier=default_tier,  # Set the default tier
            )

            # custom logic to generate thumbnails, expiration links, etc., goes here.
            # Example: Generate thumbnails and save them if needed.
            # Example: Generate an expiration link if the user specified it.

            return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
