from dataclasses import dataclass
from typing import List


@dataclass
class GeoObject:
    pos: str


@dataclass
class Feature:
    geometry: dict
    properties: dict


@dataclass
class GeoJSON:
    features: List[Feature]


@dataclass
class YandexData:
    response: dict
