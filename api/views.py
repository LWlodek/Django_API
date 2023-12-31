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

            # Check the image format using PIL (Pillow)
            try:
                img = PILImage.open(uploaded_image)
                img_format = img.format.upper()

                # Only allow JPEG and PNG formats
                if img_format not in ['JPEG', 'PNG']:
                    return Response({'error': 'Invalid image format'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': 'Invalid image format'}, status=status.HTTP_400_BAD_REQUEST)

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

            # Generate and save the 200px thumbnail
            generate_and_save_thumbnail(uploaded_image, image_instance, size=(200, 200))
            # Calculate and save the URLs for the 200px thumbnail
            image_instance.thumbnail_200px = settings.MEDIA_URL + image_instance.thumbnail.name

            # If the user is premium or enterprise, generate and save the 400px thumbnail
            if user_tier.name in ['Premium', 'Enterprise']:
                generate_and_save_thumbnail(uploaded_image, image_instance, size=(400, 400))
                # Calculate and save the URL for the 400px thumbnail
                image_instance.thumbnail_400px = settings.MEDIA_URL + image_instance.thumbnail.name
                image_instance.save()

            # Construct the response based on the user's plan
            response_data = {
                'message': 'Image uploaded successfully',
                'thumbnail_200px': image_instance.thumbnail_200px,
                'thumbnail_400px': image_instance.thumbnail_400px if user_tier.name != 'Basic' else None,
                'original_link': image_instance.original_link if user_tier.name != 'Basic' else None,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
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


# class ExpiringLinkView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request, image_id):
#         # Ensure the user is an Enterprise user
#         if request.user.tier.name != 'Enterprise':
#             return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
#
#         # Retrieve the image instance by ID
#         try:
#             image = Image.objects.get(id=image_id)
#         except Image.DoesNotExist:
#             return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         # Deserialize and validate the expiration time
#         serializer = ExpiringLinkSerializer(data=request.data)
#         if serializer.is_valid():
#             expiration_seconds = serializer.validated_data['expiration_seconds']
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         # Generate the expiring link (You need to implement this method in the model)
#         expiring_link = image.generate_expiring_link(expiration_seconds)
#
#         # Return the expiring link
#         return Response({'expiring_link': expiring_link}, status=status.HTTP_200_OK)