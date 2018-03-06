from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

class Profile(models.Model):
    """docstring for Person"""
    """ 기억할 인물에 대한 설명 """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField('', upload_to='person_profile/%Y/%m/',
                     null=True, blank=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)

    @property
    def positions_count(self):
        user = self.user
        return user.positions.count()

    @property
    def pictures_count(self):
        user = self.user
        pictures = user.picture_set.all()
        print("Pictures : ", pictures)
        return user.picture_set.count()

def create_user_profile(sender, instance, created, **kwargs):
    print("Create User Profile")
    if created:
        Profile.objects.create(user=instance, nickname=instance.first_name)

def save_user_profile(sender, instance, **kwargs):
    print("Save User Profile")
    instance.profile.save()

post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
post_save.connect(save_user_profile, sender=settings.AUTH_USER_MODEL)