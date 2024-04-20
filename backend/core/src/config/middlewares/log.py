import logging

from rest_framework.request import Request

logger = logging.getLogger(__name__)


class LogUnexpectedErrorMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request: Request):
        response = self._get_response(request)
        return response

    def process_exception(self, request: Request, exception: Exception):
        logger.error(
            exception,
            extra={
                'view': request.resolver_match._func_path,
                'session_id': request.session._SessionBase__session_key,
            },
        )
