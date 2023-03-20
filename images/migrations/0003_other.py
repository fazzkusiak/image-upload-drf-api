
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_expiringlink'),
    ]

    operations = [

	]
from ..models import Tier, User
if not Tier.objects.first():
    Tier.objects.create(name="Basic")
    Tier.objects.create(name="Premium", thumbnail_400px=True, source_image=True)
    Tier.objects.create(
        name="Enterprise",
        thumbnail_400px=True,
        source_image=True,
        fetch_link=True,
    )
if not User.objects.filter(is_superuser=True):
    User.objects.create_superuser(
    username="admin", password="admin", tier=Tier.objects.get(id=3))
 

