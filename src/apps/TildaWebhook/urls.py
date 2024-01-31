from django.urls import path
from ...api.v1.TildaWebhook.views import BaseTildaWebhookView


urlpatterns = [
    path('tilda-webhook/', BaseTildaWebhookView.as_view(), name='tilda-webhook'),
]
