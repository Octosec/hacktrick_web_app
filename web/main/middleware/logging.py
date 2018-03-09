from django.utils.deprecation import MiddlewareMixin
from main.utils import get_client_ip
from django.utils.cache import add_never_cache_headers
from profiles.models import Visitor
from django.contrib.sessions.models import Session

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

class OneSessionPerUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if isinstance(request.user, Profile):
            current_key = request.session.session_key
            if hasattr(request.user, 'visitor'):
                active_key = request.user.visitor.session_key
                if active_key != current_key:
                    Session.objects.filter(session_key=active_key).delete()
                    request.user.visitor.session_key = current_key
                    request.user.visitor.save()
            else:
                Visitor.objects.create(
                    user=request.user,
                    session_key=current_key,
                )

class DisableCacheIfLoginUser(MiddlewareMixin):
    
    def process_response(self, request, response):
        if request.user.is_authenticated():
            add_never_cache_headers(response)
        return response
