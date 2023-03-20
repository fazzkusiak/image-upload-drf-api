from django.test import TestCase
from ..models import Tier, Photo, User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
class TierModelTests(TestCase):
    def setUp(self):
        self.tier1 = Tier.objects.create(name="Tier 1")
        self.tier2 = Tier.objects.create(name="Tier 2", thumbnail_400px=True, source_image=True)

    def test_tier_str_method(self):
        self.assertEqual(str(self.tier1), "Tier 1")
        self.assertEqual(str(self.tier2), "Tier 2")

    def test_tier_thumbnail_fields(self):
        self.assertTrue(self.tier1.thumbnail_200px)
        self.assertFalse(self.tier1.thumbnail_400px)
        self.assertFalse(self.tier1.source_image)
        self.assertFalse(self.tier1.fetch_link)

        self.assertTrue(self.tier2.thumbnail_200px)
        self.assertTrue(self.tier2.thumbnail_400px)
        self.assertTrue(self.tier2.source_image)
        self.assertFalse(self.tier2.fetch_link)


