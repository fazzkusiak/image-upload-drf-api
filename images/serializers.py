from rest_framework import serializers
from .models import Photo
from django.core.validators import FileExtensionValidator

class DynamicModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        if fields:
            for field_name in set(self.fields) - set(fields):
                self.fields.pop(field_name)


class PhotoCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Photo 
        fields = ("source_image",)

    def validate_source_image(self, value):
        if value.content_type not in ["image/jpeg", "image/png"]:
            raise serializers.ValidationError("Only JPEG and PNG images are allowed.")
        return value



class PhotoListSerializer(DynamicModelSerializer):
    
    owner = serializers.ReadOnlyField()
    upload_date = serializers.ReadOnlyField()
    source_image = serializers.ImageField()
    thumbnail_200px = serializers.ImageField()
    thumbnail_400px = serializers.ImageField()

    class Meta:
        model = Photo
        fields = (
            "owner",
            "upload_date",
            "source_image",
            "thumbnail_200px",
            "thumbnail_400px",
        )


