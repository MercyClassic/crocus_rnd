from rest_framework import serializers

from products.db.models import Category, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='products:api-product-detail',
        read_only=True,
        lookup_field='slug',
    )
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'url',
            'title',
            'slug',
            'image',
            'price',
        )

    def get_price(self, obj):
        return obj.price


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    kind = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'slug',
            'image',
            'images',
            'description',
            'kind',
            'price',
        )

    def get_price(self, obj):
        return obj.price

    def get_kind(self, obj):
        type_choices = {
            'bouquet': {'url': 'bouquet', 'humanized': 'Все букеты'},
            'box': {'url': 'box', 'humanized': 'Все коробки'},
            'basket': {'url': 'basket', 'humanized': 'Все корзинки'},
        }
        return type_choices.get(obj.kind)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')
