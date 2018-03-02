from django.contrib import admin
from .models import Position, Picture

# Register your models here.
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    class Meta:
        model = Position
    list_display = ['slug', 'name', 'author']
    prepopulated_fields = {'slug':('name',)} # 5


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    class Meta:
        model = Picture
    list_display = ['id', 'name', 'locname', 'lat', 'lng', 'file']
