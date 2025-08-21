from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from categories.models import Category

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    Image = None
    ImageDraw = None
    ImageFont = None


class Command(BaseCommand):
    help = "Generate placeholder images for categories"

    def add_arguments(self, parser):
        parser.add_argument('--overwrite', action='store_true')

    def handle(self, *args, **options):
        if Image is None:
            self.stderr.write(self.style.ERROR('Pillow not installed. Install with: pip install Pillow'))
            return

        target = Path(settings.MEDIA_ROOT) / 'categories'
        target.mkdir(parents=True, exist_ok=True)

        created = 0
        for cat in Category.objects.all():
            file = target / f"{cat.pk}.png"
            if file.exists() and not options['overwrite']:
                if not cat.image:
                    cat.image.name = f"categories/{file.name}"
                    cat.save(update_fields=['image'])
                continue

            img = Image.new('RGB', (1000, 320), color=(245, 247, 251))
            d = ImageDraw.Draw(img)
            title = cat.name
            try:
                font = ImageFont.truetype('DejaVuSans-Bold.ttf', 48)
            except Exception:
                font = ImageFont.load_default()
            bbox = d.textbbox((0, 0), title, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            x = (1000 - w) // 2
            y = (320 - h) // 2
            d.text((x, y), title, fill=(29, 78, 216), font=font)
            img.save(file, format='PNG')
            created += 1

            cat.image.name = f"categories/{file.name}"
            cat.save(update_fields=['image'])

        self.stdout.write(self.style.SUCCESS(f"Created/linked {created} category images"))


