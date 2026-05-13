from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='users.register'),
    path('login', views.login_view, name='users.login'),
    path('logout', views.logout_view, name='users.logout'),
]
