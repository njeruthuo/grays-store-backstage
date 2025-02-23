from rest_framework import serializers

from catalogue.models import Product, Category, Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()

    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description',
                  'brand', 'category', 'images', 'stocked']

    def create(self, validated_data):
        # Add how we will be adding images by extracting the payload (image and passing it to the image serializer)
        return super().create(validated_data)
