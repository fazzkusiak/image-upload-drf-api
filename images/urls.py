from .views import PhotoListCreateView
from django.urls import path

urlpatterns = [
    path("photos/", PhotoListCreateView.as_view(), name="photos"),
]