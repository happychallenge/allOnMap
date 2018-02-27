from django.contrib import admin
from .models import Position

# Register your models here.
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    class Meta:
        model = Position
    list_display = ['id', 'picture', 'locname', 'myname', 'lat', 'lng']
