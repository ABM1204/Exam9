from django import forms
from .models.photo import Photo
from .models.album import Album


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'album', 'is_private']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['album'].queryset = Album.objects.filter(author=user)

    def clean(self):
        cleaned_data = super().clean()
        album = cleaned_data.get('album')
        is_private = cleaned_data.get('is_private')

        if album and album.is_private:
            cleaned_data['is_private'] = True

        return cleaned_data


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'is_private']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
