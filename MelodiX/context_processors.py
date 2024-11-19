from django.conf import settings

def media_url(request):
    """Add MEDIA_URL to the template context."""
    return {'MEDIA_URL': settings.MEDIA_URL}
