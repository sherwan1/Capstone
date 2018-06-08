from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    ''' age = forms.IntegerField(required=True, help_text='Age between 18-30')
    profession = forms.CharField(required=True) '''
    email = forms.EmailField(required=True, label='Email-addr', initial='only uoft email domain allowed')
    firstname = forms.CharField(required=True)
    lastname = forms.CharField(required=True)

    class Meta():

        model = User

        fields = ('firstname','lastname', 'email', 'password')

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

class FileUploadForm(forms.Form):
    file=forms.FileField()

class GroupImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

class CourseImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


