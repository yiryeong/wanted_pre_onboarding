from django.urls import path
from .views import ProductViewSet

# Blog 목록 보여주기
product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# Blog detail 보여주기 + 수정 + 삭제
product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<int:pk>', product_detail, name='product_detail'),
]
