from rest_framework.views import exception_handler


def custom_exception_handler(excep, context):

    handlers = {
        'NotAuthenticated': _handle_authentication_error,
        'ValidationError': _handle_generic_error,
        'Http404': _handle_generic_error,
        'PermissionDenied': _handle_generic_error
    }
    response = exception_handler(excep, context)
    if response is not None:
        response.data['status_code'] = response.status_code

    exception_class = excep.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](excep, context,response)
    return response

def _handle_authentication_error(excep, context, response):
    response.data = {
        'error': 'Please login to access this page',
        'status_code': response.status_code
    }
    return response

def _handle_generic_error(excep, context, response):
    return response