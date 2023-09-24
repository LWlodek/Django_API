from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from .serializers import ImageUploadSerializer, ImageListSerializer
from images.models import Image
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)


    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_image = serializer.validated_data['image']

            # Check the content type of the uploaded image
            content_type = uploaded_image.content_type
            if not content_type.startswith('image'):
                return Response({'error': 'Invalid image format'}, status=status.HTTP_400_BAD_REQUEST)

            # Basic user uploads the original image
            user_tier = request.user.tier
            image_instance = Image.objects.create(
                user=request.user,
                tier=user_tier,
                image_file=uploaded_image
            )

            # Construct the 'original_link' field based on the saved image path
            image_instance.original_link = settings.MEDIA_URL + image_instance.image_file.name
            image_instance.save()

            # Generate and save thumbnails 200x200px
            generate_and_save_thumbnail(uploaded_image, image_instance, size=(200, 200))

            # Generate and save thumbnails 400x400px if user is premium or enterprise
            if user_tier.name in ['Premium', 'Enterprise']:
                generate_and_save_thumbnail(uploaded_image, image_instance, size=(400, 400))

            return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_and_save_thumbnail(original_image, image_instance, size=(200, 200)):
    try:
        # Parse width and height from the size parameter
        width, height = size

        img = PILImage.open(original_image)

        # Resize the image to the specified size without maintaining the aspect ratio
        img = img.resize((width, height), PILImage.BILINEAR)  # Use BILINEAR resampling filter for downsampling

        # Create a BytesIO object to store the thumbnail
        thumbnail_io = BytesIO()

        # Save the resized image to the BytesIO object with the original image format
        img.save(thumbnail_io, format=img.format or 'JPEG')  # Use 'JPEG' as the default format

        # Seek to the beginning of the BytesIO object
        thumbnail_io.seek(0)

        # Construct the filename based on the size parameter
        ################ If there will be enough time, rework naming system #####################
        filename = f'thumbnail_{width}x{height}.jpg'
        # Save the thumbnail to the appropriate field in the Image instance
        image_instance.thumbnail.save(
            filename,
            ContentFile(thumbnail_io.read()),
            save=False,  # Set save to False, to prevent recursion
        )
        image_instance.save()  # Save the Image instance with the thumbnail

    except Exception as e:
        print(f"Error processing image: {e}")


class ImageListView(generics.ListAPIView):
    serializer_class = ImageListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(user=user).order_by('-upload_datetime')