import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from shapely.geometry import Point, shape
from requests.exceptions import RequestException

from VilkaWorker.src.config.settings import YANDEX_API_KEY
from VilkaWorker.src.utils.getLogger import logger_errors, logger_events
from dto import *


def get_yandex_data(address: str) -> YandexData:
    """
    Получение данных от Yandex API по адресу.

    :param address: Адрес для запроса.
    :return: Данные от Yandex API.
    """
    yandex_api_key = YANDEX_API_KEY
    yandex_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={yandex_api_key}&format=json&geocode={address}"

    response = requests.get(yandex_url)
    response.raise_for_status()
    return YandexData(response.json())


def get_geojson_data() -> GeoJSON:
    """
    Получение данных KML карты, рассположеных на git.

    :return: Данные KML
    """
    geojson_response = requests.get(
        "https://raw.githubusercontent.com/mizanin16/geo_json/main/geo.geojson"
    )
    geojson_response.raise_for_status()
    return GeoJSON(geojson_response.json())


@csrf_exempt
def check_address(request) -> JsonResponse:
    """
    Проверка адреса на наличие в зоне.

    :param request: HTTP-запрос.
    :return: JsonResponse с результатами проверки.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        address = data.get("address", "")

        if address:
            try:
                logger_events.debug(f"Data from check_address: {address}")

                yandex_data = get_yandex_data(address)
                coordinates = yandex_data.response["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"][
                    "pos"]
                longitude, latitude = map(float, coordinates.split())

                # Проверка, были ли данные GeoJSON уже загружены
                if "geojson" not in check_address.__dict__:
                    check_address.geojson = get_geojson_data()

                point = Point(longitude, latitude)

                is_address_in_zone = any(
                    shape(feature.geometry["geometry"]).contains(point)
                    for feature in check_address.geojson.features
                )

                description = next(
                    (
                        feature.properties.get("description", "")
                        for feature in check_address.geojson.features
                        if shape(feature.geometry["geometry"]).contains(point)
                    ),
                    False,
                )

                response_data = {
                    "is_address_in_zone": is_address_in_zone,
                    "description": description,
                }
                return JsonResponse(response_data)
            except RequestException as e:
                logger_errors.exception("Error in check_address")
                return JsonResponse({"error": f"An error occurred: {e}"}, status=500)
        else:
            logger_events.debug("Data from check_address status=400")
            return JsonResponse({"error": "Address is missing"}, status=400)
