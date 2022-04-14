from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Funding
from product.models import Product
from .FundingSerializer import FundingSerializer


class FundingViewSet(viewsets.ModelViewSet):
    queryset = Funding.objects.all()
    serializer_class = FundingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        펀딩 등록
        :param request: [p : 상품]
        :param args:
        :param kwargs:
        :return:
        """
        if 'price' in request.data:
            return JsonResponse({"msg": "price field is Product one_time_funding. Can't create"},
                                status=status.HTTP_409_CONFLICT)

        if 'u' in request.data and request.data['u'] != request.user.id:
            return JsonResponse({"msg": "Can't funding with other's account"},
                                status=status.HTTP_409_CONFLICT)

        request.data['price'] = Product.objects.get(pk=request.data['p']).one_time_funding
        request.data['u'] = request.user.id

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse({"data": serializer.data, "msg": "funding successful."},
                                status=status.HTTP_201_CREATED)
