from django.db import models

# Create your models here.
class phoneModel(models.Model):
    name = models.CharField(blank=False, max_length=15)
    mobile = models.CharField(max_length=13, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return str(self.name)