from django.contrib import admin
from . import models


@admin.register(models.Tier)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','thumbnail_sizes1', 'thumbnail_sizes2',
                    'has_original_link', 'can_generate_expiring_link',) #tutaj wyswietlanie rozmiarow?