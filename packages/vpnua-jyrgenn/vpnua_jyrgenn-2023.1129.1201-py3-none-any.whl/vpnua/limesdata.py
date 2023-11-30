# Limes-related things.

import json
import urllib.request

from .basedefs import *

def limes_get(partial_url):
    """GET something from the Limes API.

    `partial_url` is relative to the configured limesapi_base URL.

    """
    url = f"{config.limesapi_base}/{partial_url}"

    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    rsp = opener.open(url)
    data = rsp.read().decode("utf-8")
    return json.loads(data)


def limes_send_template(uid, template_fname):
    """Send an email message to `uid` using the specified template.

    `template_fname` is the file name of the message template in the
    message template directory.

    """
    return limes_get(f"users/{uid}/email/template/{template_fname}")


