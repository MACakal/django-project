from django.urls import path, include
from . import views
from .models import Profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('', include('django.contrib.auth.urls')),
    path("newtime/", views.new_time, name="newtime"),
    path("register/", views.register, name="register"),
    path("time/<str:length>", views.times, name="Times"),
    path("unapproved_times/", views.unapproved_times, name="unapproved_times"),
    path("approve_time/<int:pk>", views.approve_times, name="approve_time"),
    path("deny_time/<int:pk>", views.deny_time, name="deny_time"),
    path("my_times/", views.my_times, name="my_times"),
    path('times/edit/<int:pk>/', views.edit_time, name='edit_time'),
    path("fastest_times/", views.fastest_time_per_distance, name="fastest_times"),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)