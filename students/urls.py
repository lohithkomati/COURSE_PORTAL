from django.urls import path
from .views import home, register, login_view, logout_view, application_form, dashboard

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('application/', application_form, name='application'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
]
