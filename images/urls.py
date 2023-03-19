from .views import PhotoListCreateView, RetrieveExpiringLinks, CreateListExpiringLinks
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("links/", CreateListExpiringLinks.as_view(), name="links"), 
    path("e/<str:encoded_id>/", RetrieveExpiringLinks.as_view(), name="links-retrieve"),
    path("photos/", PhotoListCreateView.as_view(), name="photos"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
