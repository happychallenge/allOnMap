from django.contrib import admin
from .models import Position, Picture
from accounts.models import Profile

# Register your models here.
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    class Meta:
        model = Position
    list_display = ['slug', 'name', 'public', 'author']
    list_editable = ['public',]
    prepopulated_fields = {'slug':('name',)} # 5


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    class Meta:
        model = Picture
    list_display = ['id', 'name', 'locname', 'lat', 'lng', 'file']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile
    list_display = ['user', 'nickname', 'picture']