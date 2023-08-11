from rest_framework import serializers

from products.models import Product, ProductImage, Category


class BaseImageSerializer(serializers.Serializer):
    # image = serializers.SerializerMethodField()

    class Meta:
        abstract = True
    #
    # def get_image(self, instance):
    #     return instance.image.url


class ProductImageSerializer(BaseImageSerializer, serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductListSerializer(BaseImageSerializer, serializers.ModelSerializer):
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


class ProductDetailSerializer(BaseImageSerializer, serializers.ModelSerializer):
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


class CategorySerializer(BaseImageSerializer, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')
