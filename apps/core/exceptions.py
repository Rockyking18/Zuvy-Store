from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """
    Returns consistent JSON error shape across all endpoints:
    { 'error': 'message', 'detail': {...} }
    Register in settings: REST_FRAMEWORK['EXCEPTION_HANDLER']
    """
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            'error': response.data if isinstance(response.data, str)
                     else response.data.get('detail', 'An error occurred'),
            'detail': response.data,
            'status_code': response.status_code,
        }
    return response
