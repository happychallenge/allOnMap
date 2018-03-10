from PIL import Image
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from .models import Profile

class ProfileForm(forms.ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    nickname = forms.CharField(label='Name')

    class Meta:
        model = Profile
        fields = [ 'nickname', 'picture', 'x', 'y', 'width', 'height', ]
        widgets = {
            'picture': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def save(self):
        profile = super(ProfileForm, self).save()

        if not profile.picture:
            return profile 

        # print(self.cleaned_data)
        if self.cleaned_data.get('x') is None:
            return profile
            
        x = int(self.cleaned_data.get('x', 0))
        y = int(self.cleaned_data.get('y'))
        width = int(self.cleaned_data.get('width'))
        height = int(self.cleaned_data.get('height'))

        image = Image.open(profile.picture)

        try:
            exif = dict(image._getexif().items())
            # print(exif)

            if exif:
                if exif[274] == 3:
                    image = image.rotate(180, expand=True)
                    image.save(profile.picture.path)
                elif exif[274] == 6:
                    image = image.rotate(270, expand=True)
                    image.save(profile.picture.path)
                elif exif[274] == 8:
                    image = image.rotate(90, expand=True)
                    image.save(profile.picture.path)
        except:
            print("There is no EXIF INFO")
        

        # new_filepath = settings.MEDIA_ROOT + profile.picture
        cropped_image = image.crop((x, y, width+x, height+y))
        resized_image = cropped_image.resize((100, 100), Image.ANTIALIAS)
        resized_image.save(profile.picture.path)

        return profile

def validate_password_strength(value):
    min_length = 8

    if len(value) < min_length:
        raise ValidationError(_('Password must be at least {0} characters long.').format(min_length))
    # check for digit
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Password must contain at least 1 digit.'))

    # check for letter
    if not any(char.isalpha() for char in value):
        raise ValidationError(_('Password must contain at least 1 letter.'))


class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.HiddenInput())
    email = forms.CharField(required=True, max_length=75)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False, label="Name", max_length=75)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password' ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password'].validators.append(validate_password_strength)
