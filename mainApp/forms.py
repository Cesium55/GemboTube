
from django import forms
from .models import User, VideoTest, Video

class AvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "avatar"
        ]
    


class VideoTestForm(forms.ModelForm):
    class Meta:
        model = VideoTest
        fields = [
            "video"
        ]


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video

        fields = [
            "originalVideo",
            "title",
            "description",
            "published",
            "thumbImage"
        ]
    