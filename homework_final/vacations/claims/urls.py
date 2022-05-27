from django.urls import path

import claims.views as claims

app_name = 'claims'

urlpatterns = [
    path('detail/<int:pk>/', claims.ClaimDetailView.as_view(), name='detail'),
    path('create/', claims.ClaimCreateView.as_view(), name='create'),
    path('update/<int:pk>/', claims.ClaimUpdateView.as_view(), name='update'),
    path('accept/<int:pk>/', claims.accept_claim, name='accept_claim'),
    path('reject/<int:pk>/', claims.reject_claim, name='reject_claim'),
]
