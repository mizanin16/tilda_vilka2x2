from typing import Optional, Union, Dict, Any
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from ....utils.getLogger import logger_errors
from ....apps.PromoCodeWorker.models import Promocode
from ....apps.TildaWebhook.models import ListAuthUsers, Delivery

ERROR_RESPONSE: Dict[str, Union[str, Any]] = {"status": "error"}
SUCCESS_RESPONSE: Dict[str, Union[str, Any]] = {"status": "success"}


def validate_param(param_name: str, value: Optional[str]) -> Response:
    if not value or not isinstance(value, str):
        return Response({**ERROR_RESPONSE, "message": f"Invalid or missing {param_name} parameter"})


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
        return Response({**ERROR_RESPONSE, "message": "Promo code already exists"})
    except Promocode.DoesNotExist:
        try:
            Promocode.objects.create(code=promo_code)
            return Response({**SUCCESS_RESPONSE, "message": "Promo code added successfully"})
        except Exception as ex:
            logger_errors.exception(f"Error creating promocode: {ex}")
            return Response({**ERROR_RESPONSE, "message": "An error occurred while adding promo code"})


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
                return Response({**ERROR_RESPONSE, "message": "User not found"})

            total_orders_count: int = sum(
                Delivery.objects.filter(phone=user.phone).count()
                for user in users_with_email
            )

            return self._handle_promocode_request(total_orders_count)

        except Exception as ex:
            logger_errors.exception(f"Error in PromocodeView.get: {ex}")
            return Response({**ERROR_RESPONSE, "message": "An error occurred while processing the request"})

    def _handle_promocode_request(self, total_orders_count: int) -> Response:
        if total_orders_count % 3 == 2 or total_orders_count == 0:
            first_promocode = Promocode.objects.first()
            if first_promocode and first_promocode.code:
                return Response({**SUCCESS_RESPONSE, "promocode": first_promocode.code})
        else:
            return Response({**SUCCESS_RESPONSE, "promocode": "No discount"})


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
        return Response({**SUCCESS_RESPONSE, "message": "Promo code removed successfully"})
    except Promocode.DoesNotExist:
        return Response({**ERROR_RESPONSE, "message": "Promo code not found"})
    except Exception as ex:
        logger_errors.exception(f"Error remove_promocode: {ex}")
        return Response({**ERROR_RESPONSE, "message": "An error occurred during removal"})
