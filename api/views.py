from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ImageUploadSerializer
from images.models import Image, Tier
from PIL import Image as PILImage  # Import PIL for image processing


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_image = serializer.validated_data['image']

            user_tier = request.user.tier
            # Create an Image instance with the user's tier
            image_instance = Image.objects.create(
                user=request.user,  # Assuming user is authenticated
                tier=user_tier,  # Associate the image with the user's tier
                image_file=uploaded_image
            )

            # custom logic to generate thumbnails, expiration links, etc., goes here.
            # Example: Generate thumbnails and save them if needed.
            # Example: Generate an expiration link if the user specified it.

            return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
