from django.contrib import admin
from .models import Position, Picture

# Register your models here.
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    class Meta:
        model = Position
    list_display = ['id', 'name', ]


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    class Meta:
        model = Picture
    list_display = ['id', 'name', 'locname', 'address', 'file']
