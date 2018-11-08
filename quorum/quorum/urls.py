
from django.contrib import admin
from django.urls import path, include
from . import views
import debito.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('debito/', include('debito.urls')),
    path('perfil/', include('perfil.urls')),
]
