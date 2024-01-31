from django.urls import path
from ...api.v1.PromoCodeWorker.views import PromocodeView


urlpatterns = [
    path('promocode/', PromocodeView.as_view(), name='promocode'),
]
