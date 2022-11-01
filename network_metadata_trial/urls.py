import logging
from django.urls import re_path, path, include
from rest_framework.decorators import api_view, renderer_classes, authentication_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


logger = logging.getLogger(__name__)


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
def up(request, format=None):
    logger.info("Happy Status")
    return Response({"status": "happy"})


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
def healthz(request, format=None):
    return Response({"status": "happy"})


urlpatterns = [
    re_path(r"^up$", up),
    re_path(r"^healthz$", healthz),
    path("v1/", include("api.v1_urls")),
]
