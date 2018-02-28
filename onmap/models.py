from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.
class Position(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField("My Name", max_length=200)
    pictures = models.ManyToManyField("Picture")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='positions')

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return "{} - {}".format(self.id, self.name)

    def get_absolute_url(self):
        return reverse('onmap:detail', args=[self.id])


class Picture(models.Model):
    """
    File and Location 
    """
    file = models.ImageField(upload_to="uploads/%Y/%m/%d/", max_length=100)
    name = models.CharField("My Name", max_length=200)
    locname = models.CharField("LocationName", max_length=200)
    address = models.CharField(max_length=100, blank=True, null=True)
    lat = models.FloatField(default=0, blank=True, null=True)
    lng = models.FloatField(default=0, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pictures')

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return "{} - {}".format(self.id, self.name)