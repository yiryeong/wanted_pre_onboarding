from django.urls import path
from .views import FundingViewSet

app_name = 'funding'

# 펀딩 목록 보여주기
funding_list = FundingViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# 펀딩 detail 보여주기 + 삭제
funding_detail = FundingViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

urlpatterns = [
    path('', funding_list, name='list'),
    path('<int:pk>', funding_detail, name='detail'),
]
