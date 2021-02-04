from rest_framework import status
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']