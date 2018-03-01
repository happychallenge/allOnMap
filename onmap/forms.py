from django import forms
from .models import Position

class PositionForm(forms.ModelForm):
    name = forms.CharField(required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'More than 2 words....'}))
    pictures = forms.ImageField(required=True, 
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Position
        fields = ['name', 'pictures', ]
