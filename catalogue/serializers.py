from rest_framework import serializers

from catalogue.models import Product, Category, Brand,Image


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


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

        print(validated_data, 'validated data')
        # Extract related fields
        request = self.context.get("request")  # Get request context
        images = request.FILES.getlist("images")  # Get uploaded images

        brand_data = validated_data.pop("brand")
        category_data = validated_data.pop("category")

        print(brand_data, 'brand')

        # Get or create brand and category
        brand, _ = Brand.objects.get_or_create(name=brand_data)
        category, _ = Category.objects.get_or_create(name=category_data)

        # Create product instance
        product = Product.objects.create(brand=brand, category=category, **validated_data)

        # Save images to Product
        for image in images:
            Image.objects.create(product=product, image=image)

        return product
