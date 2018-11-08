
from django.contrib import admin
from django.urls import path
from . import views
import debito.views

urlpatterns = [
    path('<str:vereador>/', views.perfil, name='perfil'),
    


]
