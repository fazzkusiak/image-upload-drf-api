

from django.db import models
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Photo
from .serializers import PhotoCreateSerializer, PhotoListSerializer
from rest_framework import status

# Create your views here.
class PhotoListCreateView(ListCreateAPIView):
    queryset = Photo.objects.all()
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PhotoCreateSerializer
        return PhotoListSerializer

    def get_fields(self):
        tier_fields = [field.name for field in self.request.user.tier._meta.fields
                       if isinstance(field, models.BooleanField) and getattr(self.request.user.tier, field.name)]
        return tuple(set(tier_fields) & set(self.get_serializer_class().Meta.fields))

    def get_queryset(self):
        return Photo.objects.filter(owner=self.request.user).order_by("-upload_date")

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, fields=self.get_fields())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.save(owner=request.user)
        response_data = self.get_serializer(instance=image, fields=self.get_fields()).data
        return Response(response_data, status=status.HTTP_201_CREATED)

