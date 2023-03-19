from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.conf import settings

from django.db import models
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import ExpiringLink, Photo
from .permissions import IsTierSuperuserPermission
from .serializers import (ExpiringLinksCreateSerializer,
                               ExpiringLinksListSerializer, PhotoCreateSerializer, PhotoListSerializer)
from typing import Type
from rest_framework.pagination import BasePagination

from functools import cached_property


# Create your views here.
class PhotoListCreateView(GenericAPIView):
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
        response_data = PhotoListSerializer(instance=image, fields=self.get_fields()).data
        return Response(response_data, status=status.HTTP_201_CREATED)

class CreateListExpiringLinks(ListCreateAPIView):

    permission_classes = (IsAuthenticated, IsTierSuperuserPermission)

    def get_queryset(self):
        return ExpiringLink.objects.filter(image__owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ExpiringLinksCreateSerializer
        else:
            return ExpiringLinksListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        expiration_seconds = serializer.validated_data["expiration_time"]

        link = ExpiringLink.objects.create(
            image=serializer.validated_data["image"],
            expiration_datetime=timezone.now() + timedelta(seconds=expiration_seconds),
        )

        encoded_id = urlsafe_base64_encode(force_bytes(link.id))

        full_url = request.build_absolute_uri(reverse("links-retrieve", kwargs={"encoded_id": encoded_id}))

        link.link = full_url
        link.save(update_fields=["link", "expiration_datetime"])

        return Response({"detail": full_url})



class RetrieveExpiringLinks(APIView):
    """View to process expiring link to image"""

    permission_classes = (AllowAny,)

    def get(self, request, encoded_id: str) -> redirect:
        try:
            decoded_id: str = urlsafe_base64_decode(encoded_id).decode()
            link: ExpiringLink = ExpiringLink.objects.get(id=decoded_id)
        except (ValueError, ObjectDoesNotExist):
            return Response(
                {"detail": "Link is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )

        if timezone.now() > link.expiration_datetime:
            return Response(
                {"error": "Link has expired"}, status=status.HTTP_401_UNAUTHORIZED
            )

        redirect_url: str = (
            f"{request.scheme}://{request.get_host()}{settings.MEDIA_URL}{link.image}"
        )
        return redirect(redirect_url)
