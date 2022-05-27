import myauth.views as myauth
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

app_name = 'myauth'

urlpatterns = [
    path('register/', myauth.EmployeeCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
