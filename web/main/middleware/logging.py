from django.utils.deprecation import MiddlewareMixin
from main.utils import get_client_ip
from django.utils.cache import add_never_cache_headers

class LogVariablesMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user:
            user = request.user
        else:
            user = 'anonymous'
        request.log_extra = {
            'client_ip': get_client_ip(request),
            'user': user
        }

class DisableCacheIfLoginUser(MiddlewareMixin):
    
    def process_response(self, request, response):
        if request.user.is_authenticated():
            add_never_cache_headers(response)
        return response
