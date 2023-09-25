from django.urls import path
from .views import ImageUploadView, ImageListView

urlpatterns = [
    path('upload-image/', ImageUploadView.as_view(), name='image-upload'),
    path('list/', ImageListView.as_view(), name='image-list'),
]

