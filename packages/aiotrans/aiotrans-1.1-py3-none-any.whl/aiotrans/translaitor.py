from typing import Optional

from aiotrans.cache import MemoryStorage, simple_cache
from aiotrans.enums import Transport
from aiotrans.transport import AiohttpTransport, HttpxTransport
from aiotrans.utils import parse_html


class Translaitor:
    def __init__(
        self,
        default_target: str = "en",
        default_source: str = "ru",
        transport: Transport = Transport.aiohttp,
    ):
        if transport is Transport.aiohttp:
            self.transport = AiohttpTransport()
        elif transport is Transport.httpx:
            self.transport = HttpxTransport()
        else:
            self.transport = transport

        self.default_target = default_target
        self.default_source = default_source

    @simple_cache(MemoryStorage())
    async def translate(
        self, text: str, target: Optional[str] = None, source: Optional[str] = None
    ) -> str:
        return parse_html(
            await self.transport.send(
                target or self.default_target, source or self.default_source, text
            )
        )
