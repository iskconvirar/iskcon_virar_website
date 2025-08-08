from django.db import models
import os

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.CharField(max_length=100)
    month = models.CharField(max_length=20, blank=True)
    link = models.URLField(blank=True, help_text="Optional: Add a section link like #event1")

    def __str__(self):
        return self.title


class Album(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, help_text="Optional: A short description of the album.")
    cover_image = models.ImageField(
        upload_to='album_covers/', 
        null=True, 
        blank=True, 
        help_text="Optional: A representative image for the album."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        """Delete the cover image from storage when album is deleted"""
        if self.cover_image:
            # Check if using Supabase storage
            use_supabase = os.getenv('USE_SUPABASE_STORAGE', 'False').lower() == 'true'
            if use_supabase:
                # For Supabase storage, delete the file
                self.cover_image.delete(save=False)
            else:
                # For local storage, delete the file if it exists
                if os.path.exists(self.cover_image.path):
                    os.remove(self.cover_image.path)
        super().delete(*args, **kwargs)

    @property
    def cover_image_url(self):
        """Get the URL for the cover image, works with both local and Supabase storage"""
        if self.cover_image:
            return self.cover_image.url
        return None


class GalleryImage(models.Model):
    album = models.ForeignKey(
        Album, 
        on_delete=models.CASCADE, 
        related_name='images',
        null=True,
        blank=True,
        help_text="Select the album this image belongs to."
    )
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    alt_text = models.CharField(max_length=150)
    show_in_homepage = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        """Delete the image from storage when gallery image is deleted"""
        if self.image:
            # Check if using Supabase storage
            use_supabase = os.getenv('USE_SUPABASE_STORAGE', 'False').lower() == 'true'
            if use_supabase:
                # For Supabase storage, delete the file
                self.image.delete(save=False)
            else:
                # For local storage, delete the file if it exists
                if os.path.exists(self.image.path):
                    os.remove(self.image.path)
        super().delete(*args, **kwargs)

    @property
    def image_url(self):
        """Get the URL for the image, works with both local and Supabase storage"""
        if self.image:
            return self.image.url
        return None

    class Meta:
        ordering = ['-id']