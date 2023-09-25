from django.test import TestCase
from .serializers import ImageUploadSerializer
from .image_module import create_dummy_image  # Import  dummy image function
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from rest_framework.parsers import MultiPartParser, FormParser
class ImageUploadSerializerTest(TestCase):
    def test_valid_image_upload_serializer(self):
        # Create a dummy image for testing
        dummy_image = create_dummy_image()
        buffer = BytesIO()
        dummy_image.save(buffer, format="JPEG")
        image_data = buffer.getvalue()

        # Create a SimpleUploadedFile from the dummy image data
        image = SimpleUploadedFile("test_image.jpg", image_data, content_type="image/jpeg")

        # Create a dictionary with the file data
        data = {'image': image}

        serializer = ImageUploadSerializer(data=data)

        # Check if the serializer is valid
        self.assertTrue(serializer.is_valid())

    def test_invalid_image_upload_serializer(self):
        # Create a dummy text file instead of an image
        text_data = b"file_content"
        text_file = SimpleUploadedFile("test_text.txt", text_data, content_type="text/plain")

        # Create a dictionary with the text file data
        data = {'image': text_file}

        serializer = ImageUploadSerializer(data=data)

        # Check if the serializer is not valid due to the invalid image format
        self.assertFalse(serializer.is_valid())
        self.assertIn('image', serializer.errors)