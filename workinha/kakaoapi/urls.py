from django.urls import path
from . import views

urlpatterns = [
    path('kakaoapi/', views.kakaoapi_view, name='kakaoapi'),
]
