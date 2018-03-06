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
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    public = models.BooleanField(default=True)
    pictures = models.ManyToManyField("Picture", related_name='positions')
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