from rest_framework import serializers
from .models import Photo, ExpiringLink
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
class DynamicModelSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        if fields:
            for field_name in set(self.fields) - set(fields):
                self.fields.pop(field_name)


class PhotoCreateSerializer(ModelSerializer):
    
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



class ExpiringLinksListSerializer(ModelSerializer):
    
    image = serializers.StringRelatedField()
    expiration_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ExpiringLink
        fields = ("image", "link", "expiration_datetime")
        read_only_fields = ("link", "expiration_datetime")


class UserImagePrimaryKeyRelatedField(PrimaryKeyRelatedField):
    
    def get_queryset(self):
        user = self.context["request"].user
        queryset = Photo.objects.filter(owner=user)
        return queryset


class ExpiringLinksCreateSerializer(ModelSerializer):
    
    expiration_time = serializers.IntegerField(min_value=300, max_value=30000)
    image = UserImagePrimaryKeyRelatedField()

    class Meta:
        model = ExpiringLink
        fields = ("id", "image", "expiration_time")
        read_only_fields = ("id",)
