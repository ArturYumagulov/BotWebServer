from django.urls import path
from . import views

urlpatterns = [
    path('<str:email>/', views.index, name='index'),
    path('vcard/<int:pk>/download/', views.download_vcard_with_photo, name='download_vcard')
]