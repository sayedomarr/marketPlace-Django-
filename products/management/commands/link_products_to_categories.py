import random
from django.core.management.base import BaseCommand
from products.models import Product
from categories.models import Category


class Command(BaseCommand):
    help = "Link existing products randomly to existing categories"

    def handle(self, *args, **options):
        categories = list(Category.objects.all())
        if not categories:
            self.stderr.write(self.style.ERROR('No categories found. Seed categories first.'))
            return

        updated = 0
        for p in Product.objects.all():
            if p.category_id:
                continue
            p.category = random.choice(categories)
            p.save(update_fields=['category'])
            updated += 1
        self.stdout.write(self.style.SUCCESS(f"Linked {updated} products to categories"))


