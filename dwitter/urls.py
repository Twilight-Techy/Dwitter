from django.contrib.auth import views as auth_views
from django.urls import path

from .views import dashboard, profile, profile_list, signup, login_view, logout_view

app_name = "dwitter"

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
]
