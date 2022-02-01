import base64
import os
from io import BytesIO
from urllib.parse import urljoin, urlparse

import requests
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict=None):
    if context_dict is None:
        context_dict = {}
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(html, result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        raise Http404(pdf.err)


def fetch_resources(uri, rel):
    if uri.startswith('http'):
        uri = urljoin(uri, urlparse(uri).path)  # if some query exist, remove last
        response = requests.get(uri)
        b64 = "data:" + response.headers['Content-Type'] + ";" + "base64," + base64.b64encode(
            response.content).decode("utf-8")
        return b64
    elif uri.startswith('/media/'):
        return os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    else:
        return finders.find(uri)
