from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ReleaseForm, TrackForm, LabelForm, ArtistForm
from .models import User, Release, Track, Store, Label, Artist
from django_otp.util import random_hex


# ----------------------------
# User Authentication Views
# ----------------------------

def register_view(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Handles user login with support for username or email."""
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username_or_email = form.cleaned_data.get('username', '').strip().lower()
        password = form.cleaned_data.get('password', '').strip()

        if '@' in username_or_email:
            try:
                user = User.objects.get(email__iexact=username_or_email)
                username = user.username
            except User.DoesNotExist:
                messages.error(request, "No account found with this email address.")
                return render(request, 'login.html', {'form': form})
        else:
            username = username_or_email

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            remember_me = request.POST.get('remember_me')
            request.session.set_expiry(1209600 if remember_me else 0)
            if TOTPDevice.objects.filter(user=user).exists():
                return redirect('verify_two_factor')
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard_view(request):
    """Displays the dashboard for logged-in users."""
    user = request.user
    profile_picture = user.profile_picture.url if user.profile_picture else '/static/default-profile.png'
    return render(request, 'dashboard.html', {'username': user.username, 'profile_picture': profile_picture})


def forgot_password_view(request):
    """Handles the forgot password page."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            messages.success(request, "Password reset instructions have been sent to your email.")
            return render(request, 'password/reset_confirmation.html')
        else:
            messages.error(request, "Please enter a valid email address.")
    return render(request, 'password/forgot.html')


@login_required
def logout_view(request):
    """Logs out the user and displays the logout page."""
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, 'logout.html')


# ----------------------------
# Two-Factor Authentication Views
# ----------------------------

@login_required
def setup_two_factor(request):
    """Handles the setup of two-step authentication."""
    user = request.user
    device, created = TOTPDevice.objects.get_or_create(user=user, name="Default")

    if request.method == 'POST':
        otp = request.POST.get('otp', '').strip()
        if otp and device.verify_token(otp):
            device.confirmed = True
            device.save()
            messages.success(request, "Two-step authentication setup successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    qr_code_url = device.config_url
    return render(request, 'setup_two_factor.html', {'qr_code_url': qr_code_url})


@login_required
def verify_two_factor(request):
    """Handles two-step authentication verification."""
    if request.method == 'POST':
        otp = request.POST.get('otp', '').strip()
        device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()

        if otp and device and device.verify_token(otp):
            request.session['two_factor_authenticated'] = True
            messages.success(request, "Authentication successful.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_two_factor.html')


@login_required
def resend_two_factor(request):
    """Resends the two-factor authentication code."""
    user = request.user
    device = TOTPDevice.objects.filter(user=user, confirmed=True).first()

    if device:
        messages.info(request, "Please open your authenticator app for a new code. Resend is not required.")
    return redirect('verify_two_factor')


# ----------------------------
# Profile View
# ----------------------------

def profile_view(request, username):
    """Displays the public profile of a user."""
    user = get_object_or_404(User, username=username)
    profile_picture = user.profile_picture.url if user.profile_picture else '/media/profile_pictures/default_user.png'
    return render(request, 'profile.html', {
        'profile_picture': profile_picture,
        'name': user.get_full_name() or user.username,
        'username': user.username,
        'member_since': user.date_joined.strftime('%B %d, %Y'),
    })


# ----------------------------
# Release Creation Views
# ----------------------------

@login_required
def create_release(request):
    """Handles initial release creation."""
    if request.method == "POST":
        title = request.POST.get("release_title")
        if not title:
            messages.error(request, "Release title is required.")
            return redirect("dashboard")

        release = Release.objects.create(
            created_by=request.user,
            title=title
        )
        return redirect('create_release_step_1', release_id=release.release_id)

    messages.error(request, "Invalid request.")
    return redirect("dashboard")


@login_required
def create_release_step_1(request, release_id):
    """Step 1: Basic Release Information."""
    release = get_object_or_404(Release, release_id=release_id, created_by=request.user)

    if request.method == 'POST':
        form = ReleaseForm(request.POST, request.FILES, instance=release)
        if form.is_valid():
            form.save()
            messages.success(request, "Step 1 complete. Proceed to Step 2.")
            return redirect('create_release_step_2', release_id=release_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReleaseForm(instance=release)

    return render(request, 'release/create_step_1.html', {'form': form, 'release': release})


@login_required
def create_release_step_2(request, release_id):
    """Step 2: Add Tracks."""
    release = get_object_or_404(Release, release_id=release_id, created_by=request.user)

    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.release = release
            track.created_by = request.user
            track.save()
            messages.success(request, "Track added successfully.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TrackForm()

    tracks = release.tracks.all()
    return render(request, 'release/create_step_2.html', {'form': form, 'release': release, 'tracks': tracks})


@login_required
def create_release_step_3(request, release_id):
    """Step 3: Store Selection and Finalization."""
    release = get_object_or_404(Release, release_id=release_id, created_by=request.user)

    if request.method == 'POST':
        release.is_active = True
        release.save()
        messages.success(request, "Release finalized successfully.")
        return redirect('dashboard')

    stores = Store.objects.all()
    return render(request, 'release/create_step_3.html', {'release': release, 'stores': stores})


# ----------------------------
# Label and Artist Management Views
# ----------------------------

@login_required
def add_label(request):
    """Handles adding a new label."""
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            label = form.save(commit=False)
            label.created_by = request.user
            label.save()
            messages.success(request, "Label added successfully.")
            return redirect('manage_labels')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LabelForm()
    return render(request, 'labels/add_label.html', {'form': form})


@login_required
def manage_labels(request):
    """Handles managing existing labels."""
    labels = Label.objects.all()
    return render(request, 'labels/manage_labels.html', {'labels': labels})


@login_required
def edit_label(request, label_id):
    """Handles editing a label."""
    label = get_object_or_404(Label, id=label_id)
    if request.method == 'POST':
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, "Label updated successfully.")
            return redirect('manage_labels')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LabelForm(instance=label)
    return render(request, 'labels/edit_label.html', {'form': form, 'label': label})


@login_required
def delete_label(request, label_id):
    """Handles deleting a label."""
    label = get_object_or_404(Label, id=label_id)
    if request.method == 'POST':
        label.delete()
        messages.success(request, "Label deleted successfully.")
        return redirect('manage_labels')
    return render(request, 'labels/delete_label.html', {'label': label})


@login_required
def add_artist(request):
    """Handles adding a new artist."""
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            artist = form.save(commit=False)
            artist.created_by = request.user
            artist.save()
            messages.success(request, "Artist added successfully.")
            return redirect('manage_artists')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ArtistForm()
    return render(request, 'artist/add_artist.html', {'form': form})


@login_required
def manage_artists(request):
    """Handles managing existing artists."""
    artists = Artist.objects.all()
    return render(request, 'artist/manage_artists.html', {'artists': artists})


@login_required
def edit_artist(request, artist_id):
    """Handles editing an artist."""
    artist = get_object_or_404(Artist, id=artist_id)
    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            form.save()
            messages.success(request, "Artist updated successfully.")
            return redirect('manage_artists')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ArtistForm(instance=artist)
    return render(request, 'artist/edit_artist.html', {'form': form, 'artist': artist})


@login_required
def delete_artist(request, artist_id):
    """Handles deleting an artist."""
    artist = get_object_or_404(Artist, id=artist_id)
    if request.method == 'POST':
        artist.delete()
        messages.success(request, "Artist deleted successfully.")
        return redirect('manage_artists')
    return render(request, 'artist/delete_artist.html', {'artist': artist})


# ----------------------------
# Custom 404 View
# ----------------------------

def custom_404_view(request, exception):
    """Handles custom 404 error page."""
    return render(request, 'errors/404.html', status=404)
