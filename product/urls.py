from django.urls import path
from . import views


app_name = 'product'

urlpatterns = [
    # django.contrib.auth 앱의 LoginView 클래스를 활용 했으므로 별도의 views.py 파일 수정이 필요 없음!
    # LoginView는 registration/login.html 를 기본으로 호출한다.
    path('', views.product, name='product'),
    path('<product_id>', views.detail_product, name='detail_product'),
]
