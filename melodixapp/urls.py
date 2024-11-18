from django.urls import path
from . import views

urlpatterns = [
    # User authentication and account management
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Protected dashboard view
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Forgot password flow
    path('password/forgot/', views.forgot_password_view, name='password_forgot'),

    # Two-Step Authentication
    path('two_factor/setup/', views.setup_two_factor, name='setup_two_factor'),
    path('two_factor/verify/', views.verify_two_factor, name='verify_two_factor'),
    path('two_factor/resend/', views.resend_two_factor, name='resend_two_factor'),
]
