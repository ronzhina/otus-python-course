import claims.views as claims
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', claims.HomePageView.as_view(), name='main'),
    path('cabinet/', claims.ClaimListView.as_view(), name='claim_list'),
    path('approve/', claims.ClaimApproveListView.as_view(), name='claim_approve_list'),
    path('claim/', include('claims.urls', namespace='claims')),
    path('myauth/', include('myauth.urls', namespace='myauth')),

    path('admin/', admin.site.urls),
]
