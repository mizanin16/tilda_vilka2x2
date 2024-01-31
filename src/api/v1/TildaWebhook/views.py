from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from django.utils import timezone
from ....utils.numbers import edit_phone
from ....apps.TildaWebhook.models import ListAuthUsers
from ..PromoCodeWorker.views import remove_promocode
from ....apps.TildaWebhook.serializers import DeliverySerializer, ListAuthUsersSerializer, PromocodeSerializer
from typing import Optional, Dict, Any


class SerializerFacade:
    @staticmethod
    def create(serializer_class: Any, data: Dict[str, Any]) -> Any:
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer


class BaseTildaWebhookView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @parser_classes([JSONParser])
    def post(request) -> Response:
        try:
            data_from_tilda: Dict[str, Any] = request.data
            if "email" in data_from_tilda:
                BaseTildaWebhookView._process_email_data(data_from_tilda)
            elif "promo_code" in data_from_tilda:
                BaseTildaWebhookView._process_promo_code_data(data_from_tilda)
            else:
                BaseTildaWebhookView._process_delivery_data(data_from_tilda)

            return Response({"status": "success"})

        except Exception:
            return Response({"status": "json error", 'message': 'An error occurred while processing the request'})

    @staticmethod
    def _process_email_data(data_from_tilda: Dict[str, Any]) -> None:
        email: str = data_from_tilda.get("email", "").lower()
        if not email:
            return

        user: Optional[ListAuthUsers] = ListAuthUsers.objects.filter(email=email).first()

        if user:
            user.name = data_from_tilda.get("name", "")
            user.phone = data_from_tilda.get("phone", "")
            user.save()
        else:
            filtered_data: Dict[str, Any] = {
                "name": data_from_tilda.get("name", ""),
                "email": email,
                "phone": edit_phone(data_from_tilda.get("phone", "")),
            }
            BaseTildaWebhookView._create_serializer(ListAuthUsersSerializer, filtered_data)

    @staticmethod
    def _process_promo_code_data(data_from_tilda: Dict[str, Any]) -> None:
        promo_code: str = data_from_tilda.get("promo_code", "")
        if promo_code:
            filtered_data: Dict[str, Any] = {"code": promo_code}
            BaseTildaWebhookView._create_serializer(PromocodeSerializer, filtered_data)

    @staticmethod
    def _process_delivery_data(data_from_tilda: Dict[str, Any]) -> None:
        filtered_data: Dict[str, Any] = {
            "address": data_from_tilda.get("address", ""),
            "name": data_from_tilda.get("Name", ""),
            "phone": edit_phone(data_from_tilda.get("Phone", "")),
            "datetime_order": timezone.now(),
        }

        if data_from_tilda.get("deliverytype") == "Самовывоз":
            filtered_data["address"] = "Самовывоз"

        payment_data: Dict[str, Any] = data_from_tilda.get("payment", {})
        promocode: str = payment_data.get("promocode", "")
        if promocode:
            remove_promocode(promocode)

        BaseTildaWebhookView._create_serializer(DeliverySerializer, filtered_data)

    @staticmethod
    def _create_serializer(serializer_class: Any, data: Dict[str, Any]) -> None:
        serializer: Any = SerializerFacade.create(serializer_class, data)
        serializer.save()


class AddUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        try:
            data: Dict[str, Any] = request.data
            email: str = data.get('email', '').lower()
            name: str = data.get('name', '')
            phone: str = edit_phone(data.get('phone', ''))
            user = ListAuthUsers.objects.filter(email=email, phone=phone).first()

            if user:
                return Response({'status': 'error', 'message': 'User with given email and phone already exists'})

            filtered_data: Dict[str, Any] = {
                'name': name,
                'email': email,
                'phone': phone,
            }

            serializer = ListAuthUsersSerializer(data=filtered_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'success', 'message': 'User added successfully'})
            else:
                return Response({'status': 'error', 'errors': serializer.errors})

        except Exception:
            return Response({'status': 'error', 'message': 'An error occurred while processing the request'})
