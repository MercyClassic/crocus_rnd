from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='products:product-detail',
        read_only=True,
        lookup_field='slug',
    )
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('slug', 'image', 'url', 'title', 'description', 'price')

    def get_image(self, obj):
        return obj.image.url
