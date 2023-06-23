import hashlib
import hmac

from django.conf import settings


def signature(**kwargs):
    params = {}
    for k, v in kwargs.items():
        params[k] = v
    keys = list(params.keys())
    keys.sort()
    sorted_params = {i: params[i] for i in keys}
    string = ""
    for k, v in sorted_params.items():
        string = f"{string}{k}{v}"
    return hmac.new(settings.FLOW_SECRET_KEY.encode(), string.encode(), hashlib.sha256).hexdigest()
