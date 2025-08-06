from django.contrib import admin
from .models import Event, Album, GalleryImage



class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 3 
    fields = ['image', 'title', 'alt_text', 'show_in_homepage']

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [GalleryImageInline]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'month')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'show_in_homepage')
    list_filter = ('album', 'show_in_homepage')