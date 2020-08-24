from django.urls import path
from rest_framework.routers import DefaultRouter
from backend.products.api import views


router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename="category-list")
router.register(r'products', views.ProductViewSet, basename="products-list")

urlpatterns = router.urls
