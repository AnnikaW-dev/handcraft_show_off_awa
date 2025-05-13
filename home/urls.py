from django.urls import path
from .views import Index
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Index.as_view(), name='home')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
