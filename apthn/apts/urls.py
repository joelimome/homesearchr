from django.conf.urls.defaults import *

urlpatterns = patterns('',
        (r'^breakdown/?$', 'apthn.apts.views.count_breakdowns'),
        (r'^count/?$', 'apthn.apts.views.count_apts'),
        (r'^get/(\w+)/?$', 'apthn.apts.getapts.getapts'),
        (r'^clean/?$', 'apthn.apts.views.clean_apts'),
)
