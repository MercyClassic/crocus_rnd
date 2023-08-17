from rest_framework import serializers

from products.models import Product, ProductImage, Category


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api-product-detail',
        read_only=True,
        lookup_field='slug',
    )

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


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')
