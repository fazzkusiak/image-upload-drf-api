from __future__ import annotations
from PIL import Image
from django.core.files import File
from io import BytesIO
import uuid
import os

from django.contrib.auth.models import AbstractUser
from django.db import models



class Tier(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    thumbnail_200px = models.BooleanField(default=True)
    thumbnail_400px = models.BooleanField(default=False)
    source_image = models.BooleanField(default=False)
    fetch_link = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class User(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.PROTECT)

    def __str__(self):
        return self.username


class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    source_image = models.ImageField(upload_to="source",blank=False)
    thumbnail_200px = models.ImageField(upload_to="200px",null=True,blank=True)
    thumbnail_400px = models.ImageField(upload_to="400px", null=True, blank=True)

    def __str__(self):
        return self.source_image.name
        
    def create_thumbnail(self, thumbnail_height, field):
        with Image.open(self.source_image) as img:
            width = round((thumbnail_height / img.height) * img.width)
            thumb = img.resize((width, thumbnail_height))
            thumbnail_name, thumbnail_extension = os.path.splitext(self.source_image.name)
            thumbnail_name = f"{thumbnail_name}_{thumbnail_height}px{thumbnail_extension}"

            if thumbnail_extension.lower() in [".jpg", ".jpeg"]:
                format_specifier = "JPEG"
            else:
                format_specifier = "PNG"

            with BytesIO() as temp_storage:
                thumb.save(temp_storage, format_specifier)
                field.save(f"{thumbnail_name}", File(temp_storage), save=False)

    def save(self, *args, **kwargs):
        if self.owner.tier.thumbnail_200px:
            self.create_thumbnail(200, self.thumbnail_200px)
        if self.owner.tier.thumbnail_400px:
            self.create_thumbnail(400, self.thumbnail_400px)

        super().save(*args, **kwargs)


    
class ExpiringLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    image = models.ForeignKey(
        Photo, on_delete=models.CASCADE, help_text="Image")
    link = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration_datetime = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.link}"
