from django.contrib import admin
from django.urls import path, include

from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name="home"),
    path('user/', include('users.urls')),
    path('academics/', include('academics.urls')),
    path('attendance/', include('attendance.urls')),

]

from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
