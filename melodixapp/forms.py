from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Release, Track, Label, Genre, Artist, Subgenre, Store

# ----------------------------
# User Forms
# ----------------------------

# Use the custom user model
User = get_user_model()


class RegisterForm(UserCreationForm):
    """Form for registering a new user."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        }),
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean_email(self):
        """Ensure the email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class LoginForm(forms.Form):
    """Form for user login."""
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email',
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label="Remember Me",
    )


# ----------------------------
# Release Forms
# ----------------------------

class ReleaseForm(forms.ModelForm):
    """Form for creating or updating a music release."""
    primary_artists = forms.ModelMultipleChoiceField(
        queryset=Artist.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )
    featuring_artists = forms.ModelMultipleChoiceField(
        queryset=Artist.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    subgenre = forms.ModelChoiceField(
        queryset=Subgenre.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Release
        fields = [
            'title', 'version', 'primary_artists', 'featuring_artists',
            'label', 'release_format', 'upc_ean', 'catalogue_number',
            'copyright_holder', 'copyright_year', 'production_holder',
            'production_year', 'artwork', 'genre', 'subgenre', 'language',
            'release_date', 'availability_date', 'price_tier'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Release Title'}),
            'version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Version/Subtitle'}),
            'upc_ean': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UPC/EAN'}),
            'catalogue_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Catalogue Number'}),
            'copyright_holder': forms.TextInput(attrs={'class': 'form-control'}),
            'copyright_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'production_holder': forms.TextInput(attrs={'class': 'form-control'}),
            'production_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'artwork': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'availability_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


# ----------------------------
# Track Forms
# ----------------------------

class TrackForm(forms.ModelForm):
    """Form for managing tracks in a release."""
    artist = forms.ModelMultipleChoiceField(
        queryset=Artist.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    subgenre = forms.ModelChoiceField(
        queryset=Subgenre.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Track
        fields = [
            'title', 'version', 'type', 'is_instrumental', 'file',
            'artist', 'isrc', 'genre', 'subgenre', 'language', 'lyrics_language',
            'lyrics', 'production_year', 'copyright_holder',
            'copyright_year', 'sound_recording_copyright',
            'parental_advisory'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Track Title'}),
            'version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Version/Subtitle'}),
            'isrc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISRC'}),
            'lyrics_language': forms.TextInput(attrs={'class': 'form-control'}),
            'lyrics': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'production_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'copyright_holder': forms.TextInput(attrs={'class': 'form-control'}),
            'copyright_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'sound_recording_copyright': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ----------------------------
# Store Forms
# ----------------------------

class StoreForm(forms.ModelForm):
    """Form for managing digital stores (admin use)."""
    class Meta:
        model = Store
        fields = ['name', 'logo', 'store_type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Store Name'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'store_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ----------------------------
# Label Forms
# ----------------------------

class LabelForm(forms.ModelForm):
    """Form for adding and managing labels."""
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Label Name'
        })
    )

    class Meta:
        model = Label
        fields = ['name']


# ----------------------------
# Artist Forms
# ----------------------------

class ArtistForm(forms.ModelForm):
    """Form for adding and managing artists."""
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Artist Name'
        })
    )

    class Meta:
        model = Artist
        fields = ['name']
