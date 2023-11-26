from enum import Enum

from aiotrans.transport import AiohttpTransport, HttpxTransport


class Transport(Enum):
    aiohttp = AiohttpTransport
    httpx = HttpxTransport
