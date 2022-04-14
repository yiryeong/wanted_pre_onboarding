from rest_framework import serializers
from .models import Product


# product update can't modify target_amount
class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'one_time_funding', 'end_date')


class ProductCreateSerializer(ProductUpdateSerializer):
    class Meta:
        model = Product
        fields = ProductUpdateSerializer.Meta.fields + ('target_amount', 'u',  'create_date',)


class ProductListSerializer(ProductCreateSerializer):
    total_funding = serializers.IntegerField(read_only=True)
    achievement_rate = serializers.CharField(read_only=True)
    d_day = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = ProductCreateSerializer.Meta.fields + ('username', 'total_funding', 'achievement_rate', 'd_day')


class ProductRetrieveSerializer(ProductListSerializer):
    participants_num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ProductListSerializer.Meta.fields + ('participants_num',)
