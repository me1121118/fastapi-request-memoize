import functools
import inspect
from contextvars import ContextVar
from typing import Dict, Any, Callable, Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_request_cache: ContextVar[Optional[Dict[str, Any]]] = ContextVar("request_memoize_cache", default=None)

class RequestMemoizeMiddleware(BaseHTTPMiddleware):
    """Initializes per-request memoization dictionary in contextvars."""

    async def dispatch(self, request: Request, call_next) -> Response:
        token = _request_cache.set({})
        try:
            return await call_next(request)
        finally:
            _request_cache.reset(token)

def request_memoize(func: Callable) -> Callable:
    """Decorator to cache return values for the duration of the current request."""
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache = _request_cache.get()
            if cache is None:
                return await func(*args, **kwargs)

            cache_key = f"{func.__qualname__}:{args}:{sorted(kwargs.items())}"
            if cache_key in cache:
                return cache[cache_key]

            result = await func(*args, **kwargs)
            cache[cache_key] = result
            return result
        return async_wrapper
    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache = _request_cache.get()
            if cache is None:
                return func(*args, **kwargs)

            cache_key = f"{func.__qualname__}:{args}:{sorted(kwargs.items())}"
            if cache_key in cache:
                return cache[cache_key]

            result = func(*args, **kwargs)
            cache[cache_key] = result
            return result
        return sync_wrapper
