from django.db import models

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
    cover_image = models.ImageField(upload_to='album_covers/', null=True, blank=True, help_text="Optional: A representative image for the album.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title




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