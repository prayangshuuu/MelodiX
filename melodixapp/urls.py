from django.urls import path
from . import views

urlpatterns = [
    # ----------------------------
    # User Authentication and Account Management
    # ----------------------------
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ----------------------------
    # Dashboard
    # ----------------------------
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # ----------------------------
    # Forgot Password
    # ----------------------------
    path('password/forgot/', views.forgot_password_view, name='password_forgot'),

    # ----------------------------
    # Two-Step Authentication
    # ----------------------------
    path('two_factor/setup/', views.setup_two_factor, name='setup_two_factor'),
    path('two_factor/verify/', views.verify_two_factor, name='verify_two_factor'),
    path('two_factor/resend/', views.resend_two_factor, name='resend_two_factor'),

    # ----------------------------
    # Profile
    # ----------------------------
    path('profile/<str:username>/', views.profile_view, name='profile'),

    # ----------------------------
    # Release Creation Steps
    # ----------------------------
    path('release/create/<uuid:release_id>/step-1/', views.create_release_step_1, name='create_release_step_1'),
    path('release/create/<uuid:release_id>/step-2/', views.create_release_step_2, name='create_release_step_2'),
    path('release/create/<uuid:release_id>/step-3/', views.create_release_step_3, name='create_release_step_3'),

    # ----------------------------
    # New Release Initial Setup
    # ----------------------------
    path('release/create/', views.create_release, name='create_release'),

    # ----------------------------
    # Labels Management
    # ----------------------------
    path('labels/add/', views.add_label, name='add_label'),
    path('labels/manage/', views.manage_labels, name='manage_labels'),
    path('labels/edit/<int:label_id>/', views.edit_label, name='edit_label'),
    path('labels/delete/<int:label_id>/', views.delete_label, name='delete_label'),

    # ----------------------------
    # Artists Management
    # ----------------------------
    path('artists/add/', views.add_artist, name='add_artist'),
    path('artists/manage/', views.manage_artists, name='manage_artists'),
    path('artists/edit/<int:artist_id>/', views.edit_artist, name='edit_artist'),
    path('artists/delete/<int:artist_id>/', views.delete_artist, name='delete_artist'),
]
