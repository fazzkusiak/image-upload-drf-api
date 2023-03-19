from django.contrib import admin
from .models import Tier, Photo, User
from django.contrib.auth.admin import UserAdmin

admin.site.register(Tier)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    search_fields = ("username",)
    ordering = ("username",)
    list_display = ("username", "tier")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Additional info",
            {"fields": ("tier",)},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "tier",
                ),
            },
        ),
    )

@admin.register(Photo)

class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "upload_date",
        "source_image",
        "thumbnail_200px",
        "thumbnail_400px",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "owner",
                    "source_image",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "owner",
                    "source_image",
                ),
            },
        ),
    )