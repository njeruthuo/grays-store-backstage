from django.core.management.base import BaseCommand
from django.utils.text import slugify
from catalogue.models import Product


class Command(BaseCommand):
    help = 'Slugifies all Product names and updates the slug field.'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        for product in products:
            # slug_name = 
            product.slug = slugify(f"{product.name}-{product.pk}")
            product.save()
            self.stdout.write(f'Slugified: {product.name} → {product.slug}')
        self.stdout.write(self.style.SUCCESS(
            'All products slugified successfully.'))
