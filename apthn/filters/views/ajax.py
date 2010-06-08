import re
import datetime

from google.appengine.api import memcache
from google.appengine.ext import db

from django.http import HttpResponse
from django.utils import simplejson

from apthn.filters.models import AptFilter

from apthn.filters.views import email

price_re = re.compile(r'\$([.\d]+).*?\$([.\d]+)')
look_back = datetime.datetime.now() - datetime.timedelta(days=2)

def ajax_get_count(request):
    city = request.META['HTTP_REFERER'].split('?')[0].rstrip('/').split('/')[-1]

    locations = []
    atoms = map(float, request.POST.get('location-data').split(','))
    for i in range(0, len(atoms), 4):
        locations.append(((atoms[i], atoms[i + 1]),
                          atoms[i + 2], atoms[i + 3]))
    m = price_re.search(request.POST.get('price'))
    lprice, hprice = map(float, m.groups())
    distances = []
    for item in locations:
        distances.extend(item[1:])

    cinfo = request.POST.get('email')

    boolean_data = {}
    for key in ('cats', 'concierge', 'washerdryer', 'heat', 'hotwater',
                'brokerfee'):
        boolean_data[key] = int(request.POST[key])

    sizes = request.POST['size_data'].split(',')

    # Create Filter
    f = AptFilter(
        active = True,
        region = city.upper(),
        distance_centers = [db.GeoPt(*x[0]) for x in locations],
        distances = distances,
        price = [int(lprice), int(hprice)],
        size_names = sizes,
        size_weights = [1.0] * len(sizes),
        **boolean_data
        )
    results, scanned = email.get_matched_apartments(f, look_back)
    count = len(results)
    return HttpResponse(simplejson.dumps({'count': count, 'scanned': scanned}),
                        mimetype="application/json")
