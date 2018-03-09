import re
from datetime import datetime
from django.conf import settings
from django.db import models
from django.urls import reverse
# from django.template.defaultfilters import slugify

# Create your models here.
class Position(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField("Name", max_length=300)
    slug = models.SlugField('SLUG', unique=True, allow_unicode=True)
    ptype = models.CharField("Type", default="E", max_length=1)
    views = models.IntegerField(default=0)
    public = models.BooleanField(default=True)
    pictures = models.ManyToManyField("Picture",
        through="PositionPictures", related_name='positions')
    plikes = models.ManyToManyField("IPaddress", through="PLikes", related_name='poslikes')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='positions', blank=True, null=True)
    create_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)

    def save(self, *args, **kwargs):
        if not self.id:
            temp = re.sub('[\.\?\/\\\\(\)\[\]\*\+\{\}\^\$]', "", self.name)
            self.slug = re.sub('[\s+]', "-", temp) + "-" + datetime.now().strftime("%Y%m%d%H%M%S")
        super(Position, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.id, self.name)

    def get_absolute_url(self):
        return reverse('onmap:detail', args=[self.slug])

    def get_pictures(self):
        return self.pictures.all()[:3]

    def get_picture_count(self):
        print(self)
        return self.pictures.count()

    # @property
    # def likes(self):
    #     return self.plikes.count()


class Picture(models.Model):
    """
    File and Location 
    """
    file = models.ImageField(upload_to="uploads/%Y/%m/%d/", max_length=300)
    name = models.CharField("My Name", max_length=300)
    locname = models.CharField("LocationName", max_length=300)
    address = models.CharField(max_length=300, blank=True, null=True)
    lat = models.FloatField(default=0, blank=True, null=True)
    lng = models.FloatField(default=0, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return "{} - {}".format(self.id, self.name)


class PositionPictures(models.Model):
    position = models.ForeignKey(Position)
    picture = models.ForeignKey(Picture)

    class Meta:
        unique_together = (
            ('position', 'picture'),
        )

class IPaddress(models.Model):
    ipaddress = models.CharField(max_length=50)


class PLikes(models.Model):
    position = models.ForeignKey(Position, related_name='pp')
    ipaddress = models.ForeignKey(IPaddress)

    class Meta:
        unique_together = (
            ('position', 'ipaddress'),
        )