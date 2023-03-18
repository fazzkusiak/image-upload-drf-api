from django.db import models

class Tier(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    thumbnail_200px = models.BooleanField(default=True)
    thumbnail_400px = models.BooleanField(default=False)
    source_image = models.BooleanField(default=False)
    fetch_link = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    
class User(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.PROTECT)

    def __str__(self):
        return self.username