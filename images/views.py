from django.views.generic import ListView
from .models import Image

class ImagesListView(ListView):
    model = Image
