from datetime import datetime
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product
from .ProductSerializer import \
    ProductCreateSerializer, ProductListSerializer, ProductRetrieveSerializer, ProductUpdateSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    create_serializer_class = ProductCreateSerializer
    list_serializer_class = ProductListSerializer
    retrieve_serializer_class = ProductRetrieveSerializer
    update_serializer_class = ProductUpdateSerializer
    today = datetime.now().date()

    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]
    search_fields = ['title']
    ordering_fields = ['create_date', 'total_funding']

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
            [
                search : 제목에 검색한 문자 포함된 상품 리스트 조회
                order_by : 정렬 (생성일 or 총펀딩금액)
            ]
        :return: 200
        """
        self.get_permissions()

        queryset = self.filter_queryset(self.get_queryset())
        for qs in queryset:
            self._recombination(qs)

        serializer = self.list_serializer_class(queryset, many=True)
        return JsonResponse({"data": serializer.data, "msg": "successful."}, status=status.HTTP_200_OK)

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
            ] + u: 게시자 레코드 아이디 (로그인 계정)

        :return: 201 : 상품 등록 성공
                 400 : 등록 데이터가 유효하지 않은 경우
        """
        self.get_permissions()

        request.data['u'] = request.user.id

        serializer = self.create_serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse({"data": serializer.data, "msg": "create product successful."},
                                status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        특정 상품 조회
        :param request:
        :param pk: 상품 레코드 아이디
        :return: 200
        """
        self.get_permissions()
        qs = self._recombination(self.get_object())

        if qs:
            return JsonResponse(self.retrieve_serializer_class(qs).data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"msg": "There isn't searched product."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        상품 수정
        :param request:
            [
                title : 상품제목 ,
                description : 상품설명 ,
                one_time_funding : 1회 펀딩금액 ,
                end_date : 펀딩 종료일
            ]
        :param pk: 수정 할 상품 레코드 아이디
        :return:
                200 : 상품 수정 완료
                403 : 수정 권한이 없을 경우 = 본인이 등록한 상품이 아닐 경우 수정 불가
        """
        self.get_permissions()
        instance = self.get_object()

        # 본인이 등록한 상품인지 확인
        if instance.u == request.user:
            # 목표금액을 수정하는지 확인
            if instance.target_amount != request.data['target_amount']:
                return JsonResponse({"msg": "target_amount field can't be modified."}, status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = self.update_serializer_class(instance, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return JsonResponse({"data": serializer.data, "msg": "update product successful."},
                                        status=status.HTTP_200_OK)
        else:
            return JsonResponse({"msg": "You do not have permission to modify this product."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        """
        상품 삭제
        :param request:
        :param pk: 상품 레코드 아이디
        :return:
                204 : 정상적으로 삭제 성공
                403 : 삭제 권한이 없을 경우 = 본인이 등록한 상품이 아닐 경우 삭제 불가
        """
        self.get_permissions()
        instance = self.get_object()

        # 본인이 등록한 상품인지 확인
        if instance.u == request.user:
            self.perform_destroy(instance)
            return JsonResponse({"msg": "delete successful."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({"msg": "You do not have permission to delete this product."}, status=status.HTTP_403_FORBIDDEN)

    # 상품 등록/수정 시 필요한 필드 추가
    def _recombination(self, qs):
        qs.participants_num = qs.funding_set.all().count()
        qs.total_funding = qs.participants_num * qs.one_time_funding
        qs.d_day = (qs.end_date.date() - self.today).days
        qs.achievement_rate = "{}%".format(int((qs.total_funding / qs.target_amount) * 100))
        qs.username = qs.u.username
        return qs
