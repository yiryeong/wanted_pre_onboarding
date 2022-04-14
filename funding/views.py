from rest_framework import viewsets
from .models import Funding
from .FundingSerializer import FundingSerializer


class FundingViewSet(viewsets.ModelViewSet):
    queryset = Funding.objects.all()
    serializer_class = FundingSerializer
