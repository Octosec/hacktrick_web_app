import logging

from django.views.generic.base import TemplateView

log = logging.getLogger(__name__)
# log.error("log example", extra=self.request.log_extra)


class IndexView(TemplateView):
    template_name = 'pages/index.html'
