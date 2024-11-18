from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib import messages
from .forms import RegisterForm, LoginForm


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

    if request.method == 'POST':
        if form.is_valid():
            # Fetch cleaned data
            username_or_email = form.cleaned_data.get('username', '').strip()
            password = form.cleaned_data.get('password', '').strip()

            if not username_or_email or not password:
                messages.error(request, "Both username/email and password are required.")
                return render(request, 'login.html', {'form': form})

            # Determine if input is an email or username
            username = None
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
                remember_me = request.POST.get('remember_me', False)
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Session expires on browser close

                # Redirect to Two-Factor Authentication if required
                if TOTPDevice.objects.filter(user=user).exists():
                    return redirect('verify_two_factor')

                return redirect('dashboard')  # Redirect to dashboard if no 2FA
            else:
                messages.error(request, "Invalid username/email or password.")
        else:
            messages.error(request, "Invalid form submission. Please correct the errors.")

    return render(request, 'login.html', {'form': form})


@login_required
def dashboard_view(request):
    """Displays the dashboard for logged-in users."""
    return render(request, 'dashboard.html', {'name': request.user.username})


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
        device.refresh_token()
        messages.success(request, "A new two-factor authentication code has been sent.")

    return redirect('verify_two_factor')
