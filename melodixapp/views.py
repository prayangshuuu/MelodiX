from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import User

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
        username_or_email = form.cleaned_data.get('username', '').strip()
        password = form.cleaned_data.get('password', '').strip()

        if not username_or_email or not password:
            messages.error(request, "Both username/email and password are required.")
            return render(request, 'login.html', {'form': form})

        # Determine if input is an email or username
        if '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                messages.error(request, "User with this email does not exist.")
                return render(request, 'login.html', {'form': form})
        else:
            username = username_or_email

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # Handle "Remember Me"
            remember_me = request.POST.get('remember_me')
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks in seconds
            else:
                request.session.set_expiry(0)  # Session expires on browser close

            # Redirect to Two-Factor Authentication if required
            if TOTPDevice.objects.filter(user=user).exists():
                return redirect('verify_two_factor')

            return redirect('dashboard')  # Redirect to dashboard if no 2FA
        else:
            messages.error(request, "Invalid username/email or password.")
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard_view(request):
    """Displays the dashboard for logged-in users."""
    user = request.user
    profile_picture = (
        user.profile_picture.url if hasattr(user, 'profile_picture') and user.profile_picture else '/static/default-profile.png'
    )
    context = {
        'username': user.username,
        'profile_picture': profile_picture,
    }
    return render(request, 'dashboard.html', context)


def forgot_password_view(request):
    """Handles the forgot password page."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        if email:
            # Placeholder for email processing logic
            print(f"Password reset requested for: {email}")
            messages.success(request, "Password reset instructions have been sent to your email.")
            return render(request, 'password/reset_confirmation.html')  # Confirmation page
        else:
            messages.error(request, "Please enter a valid email address.")
    return render(request, 'password/forgot.html')


@login_required
def logout_view(request):
    """Logs out the user and displays the logout page."""
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, 'logout.html')


@login_required
def setup_two_factor(request):
    """Handles the setup of two-step authentication."""
    user = request.user

    # Check if a TOTP device already exists, create if not
    device, created = TOTPDevice.objects.get_or_create(user=user, name="Default")

    if request.method == 'POST':
        otp = request.POST.get('otp', '').strip()

        # Verify the OTP entered by the user
        if otp and device.verify_token(otp):
            messages.success(request, "Two-step authentication setup successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    # Generate the QR code dynamically
    qr_code_url = device.config_url

    return render(request, 'setup_two_factor.html', {'qr_code_url': qr_code_url})


@login_required
def verify_two_factor(request):
    """Handles two-step authentication verification."""
    if request.method == 'POST':
        otp = request.POST.get('otp', '').strip()
        device = TOTPDevice.objects.filter(user=request.user).first()

        if otp and device and device.verify_token(otp):
            messages.success(request, "Authentication successful.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_two_factor.html')


@login_required
def resend_two_factor(request):
    """Resends the two-factor authentication code."""
    user = request.user
    device = TOTPDevice.objects.filter(user=user).first()

    if device:
        messages.info(request, "Please open your authenticator app for a new code. Resend is not required.")
    return redirect('verify_two_factor')


def profile_view(request, username):
    """Displays the public profile of a user."""
    user = get_object_or_404(User, username=username)
    profile_picture = user.profile_picture.url if user.profile_picture else '/media/profile_pictures/default_user.png'
    context = {
        'profile_picture': profile_picture,
        'name': user.get_full_name() or user.username,
        'username': user.username,
        'member_since': user.date_joined.strftime('%B %d, %Y'),
    }
    return render(request, 'profile.html', context)


def custom_404_view(request, exception):
    """Handles custom 404 error page."""
    return render(request, 'errors/404.html', status=404)
