from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Position

class PositionForm(forms.ModelForm):
    name = forms.CharField(required=True, 
        widget=forms.TextInput(attrs={'placeholder': _('More than 2 words....')}))
    public = forms.BooleanField(initial=True, label=_('Do you want this posting to be public?'),
        widget=forms.CheckboxInput(attrs={'class': 'js-switch'}))
    pictures = forms.ImageField(required=True, 
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Position
        fields = ['name', 'public', 'pictures', ]
        widgets = {
            'pictures': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }


class PositionEditForm(forms.ModelForm):
    name = forms.CharField(required=True, 
        widget=forms.TextInput(attrs={'placeholder': _('More than 2 words....')}))
    public = forms.BooleanField(label=_('Do you want this posting to be public?'),
        widget=forms.CheckboxInput(attrs={'class': 'js-switch'}))

    class Meta:
        model = Position
        fields = ['name', ]
