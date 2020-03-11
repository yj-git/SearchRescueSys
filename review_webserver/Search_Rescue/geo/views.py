from django.shortcuts import render
from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from geoserver.catalog import Catalog

# Create your views here.

cat = Catalog("http://localhost:8083/geoserver/rest")


class GeoLayerView(APIView):
    def get(self, request):
        pass
