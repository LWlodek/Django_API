from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from images.models import Tier, UserProfile, Image
from unittest.mock import patch

class TierModelTest(TestCase):
    def test_tier_creation(self):
        tier = Tier.objects.create(
            name='test_tier',
            thumbnail_size='200x200',
            has_original_link=True,
            can_generate_expiring_link=True
        )
        self.assertEqual(tier.name, 'test_tier')
        self.assertEqual(tier.thumbnail_size, '200x200')
        self.assertTrue(tier.has_original_link)
        self.assertTrue(tier.can_generate_expiring_link)

class UserProfileModelTest(TestCase):
    def test_user_profile_creation(self):
        user = UserProfile.objects.create_user(username='testuser', password='testpassword')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword'))

class ImageModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword')

        # Create a test tier
        self.tier = Tier.objects.create(
            name='test_tier',
            thumbnail_size='200x200',
            has_original_link=True,
            can_generate_expiring_link=True
        )

    @patch('images.models.Image.image_file', SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"))
    def test_image_creation(self):
        # Create an image
        image = Image.objects.create(
            user=self.user,
            tier=self.tier,
            expiration_time=None,
            expiring_token=None,
            original_link=None,
            thumbnail=None,
            thumbnail_200px=None,
            thumbnail_400px=None,
        )

        self.assertEqual(image.user, self.user)
        self.assertEqual(image.tier, self.tier)
        self.assertIsNone(image.expiration_time)
        self.assertIsNone(image.expiring_token)
        self.assertIsNone(image.original_link)
        self.assertIsNone(image.thumbnail_200px)
        self.assertIsNone(image.thumbnail_400px)