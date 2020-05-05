from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from memoriais.views import home, download

urlpatterns = [
    path('admin/', admin.site.urls),
    path('download', download, name='download'),
    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
