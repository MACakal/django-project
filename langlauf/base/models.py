from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_picture:
            img = Image.open(self.profile_picture.path)

            width, height = img.size

            if width > height:
                left = (width - height) / 2
                top = 0
                right = (width + height) / 2
                bottom = height
            else:
                left = 0
                top = (height - width) / 2
                right = width
                bottom = (height + width) / 2

            img = img.crop((left, top, right, bottom))

            img = img.resize((500, 500))

            img.save(self.profile_picture.path)
    

class Distance(models.Model):
    length = models.CharField(max_length=30, blank=True, unique=True)
    full_name = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return self.length
      
      
class Time(models.Model):
    distance = models.ForeignKey(
        Distance, on_delete=models.CASCADE, null=False)
    time_in_minutes = models.IntegerField(blank=False,)
    date = models.DateField(blank=False,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='approved_by', null=True, blank=True)
    def __str__(self):
        return f"{self.distance.length} by {self.user.get_username()}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

