import functools

from django.http import HttpResponseRedirect
from google.appengine.api import users

__all__ = ('login_required',)

def login_required(method):
    @functools.wraps(method)
    def _wrapper(request, *args, **kwargs):
        if not request.user:
            return HttpResponseRedirect(users.create_login_url(request.path))
        else:
            return method(request, *args, **kwargs)
    return _wrapper
