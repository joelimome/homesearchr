from google.appengine.api import users

class AppEngineAuthMiddleware(object):
    def process_request(self, request):
        request.user = users.get_current_user()

