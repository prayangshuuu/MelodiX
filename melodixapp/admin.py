from django.contrib import admin
from .models import User, Label, Artist, Genre, Subgenre, Release, Track, Store


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')
    search_fields = ('name', 'created_by__username')
    list_filter = ('created_by',)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')
    search_fields = ('name', 'created_by__username')
    list_filter = ('created_by',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Subgenre)
class SubgenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre')
    list_filter = ('genre',)
    search_fields = ('name', 'genre__name')


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'label', 'release_format', 'is_active', 'release_date')
    list_filter = ('release_format', 'is_active', 'release_date')
    search_fields = ('title', 'label__name')
    filter_horizontal = ('primary_artists', 'featuring_artists')  # To improve M2M selection UI


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'release', 'type', 'is_instrumental', 'genre')
    list_filter = ('type', 'is_instrumental', 'genre')
    search_fields = ('title', 'release__title', 'artist__name', 'genre__name')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'store_type')
    search_fields = ('name', 'store_type')
    list_filter = ('store_type',)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
