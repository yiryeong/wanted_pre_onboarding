from django.urls import path, include
from .views import ProductViewSet


product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<int:pk>', product_detail, name='product_detail'),
]
