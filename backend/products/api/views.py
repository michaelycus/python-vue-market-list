from rest_framework import viewsets
from backend.products.models import (Category, Product)
from .serializers import (CategorySerializer, ProductSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by('name')
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('name')
    serializer_class = ProductSerializer
