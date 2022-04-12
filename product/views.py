from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product
from .ProductSerializer import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    search_fields = ['title']
    ordering_fields = ['create_date']
    ordering = ['create_date']

    # 권한 설정
    permission_classes_by_action = {
        "default": [IsAuthenticated],
        "list": [IsAuthenticated],
        "create": [IsAdminUser],
        "retrieve": [IsAuthenticated],
        "update": [IsAdminUser],
        "destroy": [IsAdminUser]
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes_by_action["default"]]

    def list(self, request):
        """
        상품 조회
        :param request:
        :return:
        """
        self.get_permissions()
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)
        return JsonResponse({"data": serializer.data, "msg": "successfully."}, status=status.HTTP_200_OK)

    def create(self, request):
        """
        상품 등록
        :param request:
            [
                title : 상품제목 ,
                description : 상품설명 ,
                target_amount : 목표금액 ,
                one_time_funding : 1회 펀딩금액 ,
                end_date : 펀딩 종료일
            ]
        :return: 201 : 상품 등록 성공
                 400 : 등록 데이터가 유효하지 않은 경우
        """
        self.get_permissions()

        insert_data = {
            "u": request.user.id,     # 로그인 상태의 계정 레코드 아이디
            "title": request.data['title'],
            "description": request.data['description'],
            "target_amount": request.data['target_amount'],
            "one_time_funding": request.data['one_time_funding'],
            "end_date": request.data['end_date']
        }
        serializer = self.serializer_class(data=insert_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse({"data": serializer.data, "msg": "create product successfully."}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
