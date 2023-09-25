from django.db import models
from django.contrib.auth.models import AbstractUser

# Define the custom Tier model for account tiers with configurable options.
class Tier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    thumbnail_size = models.CharField(max_length=255, blank=True, null=True)
    has_original_link = models.BooleanField(default=False)
    can_generate_expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class UserProfile(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True, blank=True)


# Define the Image model to store image details.
class Image(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.PROTECT)
    image_file = models.ImageField(upload_to='original/')
    upload_datetime = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DurationField(null=True, blank=True)
    expiring_token = models.CharField(max_length=100, null=True, blank=True)
    original_link = models.URLField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', default='default_thumbnail.jpg')
    thumbnail_200px = models.URLField(null=True, blank=True)
    thumbnail_400px = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Image uploaded by {self.user.username} at {self.upload_datetime}"

    # EXPIRING LINKS, not finished
    # def generate_expiring_link(self, expiration_seconds):
    #     # Calculate the expiration time as the current time plus the specified seconds
    #     expiration_time = datetime.now() + timedelta(seconds=expiration_seconds)
    #
    #     # Create a TimestampSigner instance
    #     signer = TimestampSigner()
    #
    #     # Sign the image's ID and expiration time
    #     signed_data = signer.sign(f"{self.id}:{expiration_time}")
    #
    #     # Generate the expiring link
    #     expiring_link = f"/api/expiring-link/{self.id}/{signed_data}"
    #
    #     return expiring_link