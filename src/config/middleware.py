import logging

logger = logging.getLogger('unexpected_errors')


class LogUnexpectedErrorMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(exception, extra={'view': request.resolver_match._func_path,
                                       'session_id': request.session._SessionBase__session_key})
