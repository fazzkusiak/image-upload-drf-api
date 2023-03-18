class PhotoListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "owner",
            "upload_date",
            "source_image",
            "thumbnail_200px",
            "thumbnail_400px",
        )
        read_only_fields = fields


class PhotoCreateSerializer(serializers.ModelSerializer):
    source_image = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg"])]
    )

    class Meta:
        model = Photo
        fields = ("source_image",)
