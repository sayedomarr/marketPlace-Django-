import os
import random
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.models import Product

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception as exc:  # Pillow might not be installed yet
    Image = None  # type: ignore
    ImageDraw = None  # type: ignore
    ImageFont = None  # type: ignore


class Command(BaseCommand):
    help = "Generate and assign dummy images for products without images"

    def add_arguments(self, parser):
        parser.add_argument('--overwrite', action='store_true', help='Regenerate images even if they exist or product has one')
        parser.add_argument('--count', type=int, default=None, help='Limit how many products to process')

    def handle(self, *args, **options):
        if Image is None:
            self.stderr.write(self.style.ERROR('Pillow is not installed. Install it with: pip install Pillow'))
            return

        media_dir: Path = Path(settings.MEDIA_ROOT)
        target_dir: Path = media_dir / 'products'
        target_dir.mkdir(parents=True, exist_ok=True)

        qs = Product.objects.all().order_by('id')
        if options['count']:
            qs = qs[: options['count']]

        processed = 0
        created_files = 0

        for product in qs:
            filename_stem = slugify(product.code or product.name) or f"product-{product.pk}"
            filename = f"{filename_stem}.png"
            img_path = target_dir / filename

            if product.image and not options['overwrite']:
                # Skip products that already have images
                continue

            if img_path.exists() and not options['overwrite']:
                # Assign existing file without regenerating
                product.image.name = f"products/{filename}"
                product.save(update_fields=['image'])
                processed += 1
                continue

            # Generate a pleasant pastel background color
            hue = random.randint(180, 360)
            base = random.randint(160, 210)
            background = (base, base - random.randint(10, 30), base - random.randint(0, 20))

            width, height = 800, 600
            image = Image.new('RGB', (width, height), color=background)
            drawer = ImageDraw.Draw(image)

            # Title text: product name (fallback to code)
            title = product.name or product.code
            subtitle = f"${product.price}"

            # Choose fonts (fallback to default if truetype not available)
            try:
                # Common system font; not guaranteed everywhere
                font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
                font_sub = ImageFont.truetype("DejaVuSans.ttf", 24)
            except Exception:
                font_title = ImageFont.load_default()
                font_sub = ImageFont.load_default()

            # Compute positions
            title_bbox = drawer.textbbox((0, 0), title, font=font_title)
            title_w = title_bbox[2] - title_bbox[0]
            title_h = title_bbox[3] - title_bbox[1]

            sub_bbox = drawer.textbbox((0, 0), subtitle, font=font_sub)
            sub_w = sub_bbox[2] - sub_bbox[0]
            sub_h = sub_bbox[3] - sub_bbox[1]

            # Centered positions
            title_x = (width - title_w) // 2
            title_y = height // 2 - title_h
            sub_x = (width - sub_w) // 2
            sub_y = title_y + title_h + 16

            # Draw text with a subtle shadow for readability
            shadow_offset = 2
            for dx, dy in [(shadow_offset, shadow_offset)]:
                drawer.text((title_x + dx, title_y + dy), title, fill=(0, 0, 0), font=font_title)
                drawer.text((sub_x + dx, sub_y + dy), subtitle, fill=(0, 0, 0), font=font_sub)
            drawer.text((title_x, title_y), title, fill=(255, 255, 255), font=font_title)
            drawer.text((sub_x, sub_y), subtitle, fill=(255, 255, 255), font=font_sub)

            image.save(img_path, format='PNG')
            created_files += 1

            product.image.name = f"products/{filename}"
            product.save(update_fields=['image'])
            processed += 1

        self.stdout.write(self.style.SUCCESS(f"Processed {processed} products, created {created_files} image files in {target_dir}"))


