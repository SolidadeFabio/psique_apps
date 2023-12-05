from django.urls import path
from . import views

urlpatterns = [
   path('download/<int:ca>', views.caepi, name='caepi')
]