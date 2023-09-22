from django.contrib import admin
from . import models

@admin.register(models.Image)
class AuthorAdmin2(admin.ModelAdmin):
    list_display = ('image_file',)

@admin.register(models.CustomUser)
class AuthorAdmin3(admin.ModelAdmin):
    list_display = ('username', 'tier',)

@admin.register(models.Tier)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','thumbnail_sizes1', 'thumbnail_sizes2',
                    'has_original_link', 'can_generate_expiring_link',) #tutaj wyswietlanie rozmiarow?