from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.CharField(max_length=100)
    month = models.CharField(max_length=20, blank=True)
    link = models.URLField(blank=True, help_text="Optional: Add a section link like #event1")

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    alt_text = models.CharField(max_length=150)
    show_in_homepage = models.BooleanField(default=True)

    def __str__(self):
        return self.title
