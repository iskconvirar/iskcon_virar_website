# iskconapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing_page'),
    path('login/', views.admin_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('gallery/album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
]