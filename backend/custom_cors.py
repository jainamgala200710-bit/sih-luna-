from starlette.middleware.cors import CORSMiddleware as CORSMiddleware_
from starlette.types import ASGIApp, Receive, Scope, Send
import logging

logger = logging.getLogger("custom_cors")

class CORSMiddleware(CORSMiddleware_):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        logger.debug(f"CORS middleware processing: {scope['type']} {scope.get('path', '')} method: {scope.get('method', 'N/A')}")
        await super().__call__(scope, receive, send)