from django.utils.deprecation import MiddlewareMixin
from main.utils import get_client_ip


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
