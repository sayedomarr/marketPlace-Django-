import random
from django.core.management.base import BaseCommand
from categories.models import Category


NAMES = [
    "Audio",
    "Wearables",
    "Accessories",
    "Storage",
    "Smart Home",
    "Gaming",
    "Office",
    "Cameras",
]

DESCRIPTIONS = [
    "Headphones, earbuds, speakers, and more.",
    "Smart watches, fitness trackers, and wearables.",
    "Cables, chargers, and peripherals.",
    "External SSDs, HDDs, and memory cards.",
    "Smart plugs, sensors, and lights.",
    "Mice, keyboards, controllers, and gear.",
    "Stands, lamps, and productivity tools.",
    "Action cams and webcams.",
]


class Command(BaseCommand):
    help = "Seed the database with dummy categories"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=8)
        parser.add_argument('--flush', action='store_true')

    def handle(self, *args, **options):
        count = options['count']
        if options['flush']:
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('Deleted existing categories'))

        created = 0
        for i in range(count):
            name = NAMES[i % len(NAMES)]
            desc = DESCRIPTIONS[i % len(DESCRIPTIONS)]
            obj, _ = Category.objects.get_or_create(name=name, defaults={'description': desc})
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Ensured {created} categories"))


