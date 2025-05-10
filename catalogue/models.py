from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        blank=True,
        unique=True,
        db_index=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='brand_products')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category_products')
    stocked = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Save first to ensure we have an ID
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Now create slug using the ID
        new_slug = slugify(f"{self.name}-{self.pk}")
        if self.slug != new_slug:
            self.slug = new_slug
            super().save(update_fields=['slug'])


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product-images')

    def __str__(self):
        return self.product.name
