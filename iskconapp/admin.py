from django.contrib import admin
from .models import Event, GalleryImage

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'month')
    search_fields = ('title',)

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'alt_text', 'show_in_homepage')
    list_filter = ('show_in_homepage',)
