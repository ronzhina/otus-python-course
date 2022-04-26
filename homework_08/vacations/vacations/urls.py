"""vacations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import claims.views as claims

urlpatterns = [
    path('', claims.HomePageView.as_view(), name='main'),
    path('cabinet/', claims.ClaimListView.as_view(), name='claim_list'),
    path('admin/', admin.site.urls),
    path('claim/detail/<int:pk>/', claims.ClaimDetailView.as_view(), name='claim_detail'),
    path('claim/create/', claims.ClaimCreateView.as_view(), name='claim_create'),
    path('claim/update/<int:pk>/', claims.ClaimUpdateView.as_view(), name='claim_update'),
]
