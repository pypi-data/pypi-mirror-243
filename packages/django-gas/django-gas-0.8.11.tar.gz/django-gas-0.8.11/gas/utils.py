import datetime
import json

from django.db.models import QuerySet
from django.utils.functional import Promise


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M')
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, QuerySet):
            return list(o)
        if isinstance(o, Promise):
            return str(o)
        return json.JSONEncoder.default(self, o)
