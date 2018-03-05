from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile
    list_display = ['nickname', 'picture']
