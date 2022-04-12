from django.urls import path
from . import views


app_name = 'product'

urlpatterns = [
    path('', views.product, name='product'),
    path('<product_id>', views.detail_product, name='detail_product'),
]
