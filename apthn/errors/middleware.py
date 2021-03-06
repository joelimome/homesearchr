import traceback

from django.conf import settings

from django.utils import simplejson
from django.http import HttpResponse

from google.appengine.api import mail

class FixEmailsMiddleware(object):
    def process_request(self, request):
        if request.META['HTTP_HOST'].startswith('localhost') or \
                request.META['HTTP_HOST'].startswith('dev.'):
            settings.DEBUG = True
            settings.TEMPLATE_DEBUG = True
            return None
        if request.META['REMOTE_ADDR'] in settings.DEBUG_IPS:
            settings.DEBUG = True
            settings.TEMPLATE_DEBUG = True
            return None
        if request.GET.get('DEBUG', None) == '1' and \
                request.META['REMOTE_ADDR'].startswith('18.224.'):
            settings.DEBUG = True
            settings.TEMPLATE_DEBUG = True
            return None
        settings.DEBUG = False
        settings.TEMPLATE_DEBUG = False
        return None

    def process_exception(self, request, exception):
        if settings.DEBUG:
            if request.is_ajax():
                return self.process_ajax(request)
            return
        try:
            request_repr = repr(request)
        except:
            request_repr = "Request repr() unabailable"

        msg = mail.EmailMessage(sender="HomeSearchERROR <no-reply@homesearchr.com>",
                                to="%s <%s>" % (tuple(settings.ADMINS[0])),
                                subject="Error occured on HomeSearchr!")
        msg.body = "Error:\n%s\n\n%s" % (traceback.format_exc(),
                                         request_repr)
        msg.send()
        return None

    def process_ajax(self, request):
        response = HttpResponse(simplejson.dumps({'error':
                                                      traceback.format_exc()}),
                                mimetype="application/json")
        response.status_code = 500
        return response
