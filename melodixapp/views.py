from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm


def register_view(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Handles user login with support for username or email."""
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Determine if the input is an email or username
        if '@' in username_or_email:  # Assume email if '@' is present
            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                username = None
        else:  # Otherwise, treat as username
            username = username_or_email

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # Handle "Remember Me"
            remember_me = request.POST.get('remember_me', None)
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks in seconds
            else:
                request.session.set_expiry(0)  # Session expires on browser close

            return redirect('dashboard')
        else:
            form = LoginForm(request.POST)
            form.add_error(None, 'Invalid email/username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard_view(request):
    """Displays the dashboard for logged-in users."""
    return render(request, 'dashboard.html', {'name': request.user.username})


def forgot_password_view(request):
    """Handles the forgot password page."""
    if request.method == 'POST':
        email = request.POST.get('email')

        # Placeholder for email processing logic
        print(f"Password reset requested for: {email}")
        return render(request, 'password/reset_confirmation.html')  # Confirmation page
    return render(request, 'password/forgot.html')


def logout_view(request):
    """Logs out the user and displays the logout page."""
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'logout.html')
