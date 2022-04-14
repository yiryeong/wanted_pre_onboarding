from django.urls import path
from .views import ProductViewSet


app_name = 'product'

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
    path('', product_list, name='list'),
    path('<int:pk>', product_detail, name='detail'),
]
