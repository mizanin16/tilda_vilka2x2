from dataclasses import dataclass
from jsondataclass import to_json, from_json


@dataclass
class ResponseJson:
    status: str
    message: str = ''
    promocode: str = ''
