from django.db import models

# Create your models here.
class phoneModel(models.Model):
    name = models.CharField(blank=False, max_length=15)
    mobile = models.CharField(max_length=13, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(blank=False, default=False)
    resId = models.CharField(max_length=6)

    def __str__(self):
        return str(self.name)

class userModel(models.Model):
    name = models.ForeignKey(phoneModel, on_delete=models.CASCADE)
    orders = models.CharField(max_length=20)
    profile = models.ImageField(default='profile.png')


class CardDetail(models.Model):
    name = models.CharField(max_length=15)
    cvv = models.IntegerField(default=000)
    cardNo = models.IntegerField()
    expiry = models.CharField(max_length=5)
