from PIL import Image
from django import forms

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

