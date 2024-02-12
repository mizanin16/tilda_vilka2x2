from typing import Optional, Union, Dict, Any
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from VilkaWorker.src.utils.getLogger import logger_errors
from VilkaWorker.src.apps.PromoCodeWorker.models import Promocode
from VilkaWorker.src.apps.TildaWebhook.models import ListAuthUsers, Delivery
from VilkaWorker.src.utils.dto_message import *


def validate_param(param_name: str, value: Optional[str]) -> Response:
    if not value or not isinstance(value, str):
        response_json = ResponseJson(status="error", message=f"INVALID_PARAMS:{param_name}")
        return Response(to_json(response_json))


@api_view(["POST"])
def add_promocode(request) -> Response:
    """
    Добавление промокода.
    """
    promo_code: Optional[str] = request.data.get("promo_code")
    response = validate_param("promo code", promo_code)
    if response:
        return response

    try:
        Promocode.objects.get(code=promo_code)
        response_json = ResponseJson(status="error", message="PROMOCODE_EXISTS")
        return Response(to_json(response_json))
    except Promocode.DoesNotExist:
        try:
            Promocode.objects.create(code=promo_code)
            response_json = ResponseJson(status="success", message="PROMOCODE_ADD")
            return Response(to_json(response_json))
        except Exception as ex:
            logger_errors.exception(f"Error creating promocode: {ex}")
            response_json = ResponseJson(status="error", message="PROMOCODE_NOT_ADD")
            return Response(to_json(response_json))


class PromocodeView(APIView):
    """
    Получение промокода для пользователя.
    """
    permission_classes = [AllowAny]

    def get(self, request) -> Response:
        email: Optional[str] = request.GET.get("email")
        response = validate_param("email", email)
        if response:
            return response

        try:
            users_with_email = ListAuthUsers.objects.filter(email=email)
            if not users_with_email.exists():
                response_json = ResponseJson(status="error", message="USER_NOT_FOUND")
                return Response(to_json(response_json))

            total_orders_count: int = sum(
                Delivery.objects.filter(phone=user.phone).count()
                for user in users_with_email
            )

            return self._handle_promocode_request(total_orders_count)

        except Exception as ex:
            logger_errors.exception(f"Error in PromocodeView.get: {ex}")
            response_json = ResponseJson(status="error", message="ERROR_REQUEST")
            return Response(to_json(response_json))

    def _handle_promocode_request(self, total_orders_count: int) -> Response:
        if total_orders_count % 3 == 2 or total_orders_count == 0:
            first_promocode = Promocode.objects.first()
            if first_promocode and first_promocode.code:
                response_json = ResponseJson(status="success", message='', promocode=first_promocode.code)
                return Response(to_json(response_json))
        else:
            response_json = ResponseJson(status="success", message='', promocode="No discount")
            return Response(to_json(response_json))


@api_view(["POST"])
def remove_promocode(request) -> Response:
    """
    Удаление промокода.
    """
    promo_code: Optional[str] = request.data.get("promo_code")
    response = validate_param("promo code", promo_code)
    if response:
        return response

    try:
        promocode_obj = Promocode.objects.get(code=promo_code)
        promocode_obj.delete()
        response_json = ResponseJson(status="success", message='PROMOCODE_REMOVE')
        return Response(to_json(response_json))
    except Promocode.DoesNotExist:
        response_json = ResponseJson(status="error", message="PROMOCODE_NOT_FOUND")
        return Response(to_json(response_json))
    except Exception as ex:
        response_json = ResponseJson(status="error", message="PROMOCODE_NOT_DELETE")
        return Response(to_json(response_json))
