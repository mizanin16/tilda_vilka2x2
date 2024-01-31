from django.urls import path
from ...api.v1.CheckAddress.views import check_address


urlpatterns = [
    path('check-address/', check_address, name='check-address'),
]
