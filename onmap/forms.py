from django import forms
from .models import Position

class PositionForm(forms.ModelForm):
    pictures = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Position
        fields = ['pictures', 'name']
