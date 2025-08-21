import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from products.models import Product


NAMES = [
    "Wireless Headphones",
    "Smart Watch",
    "Mechanical Keyboard",
    "4K Action Camera",
    "Bluetooth Speaker",
    "Portable SSD 1TB",
    "Noise Cancelling Earbuds",
    "Gaming Mouse",
    "USB-C Hub",
    "Laptop Stand",
    "Webcam 1080p",
    "LED Desk Lamp",
    "Smart Home Plug",
    "Fitness Tracker",
    "Drone Mini",
    "E-Reader",
    "Wireless Charger",
    "Power Bank 20k",
    "VR Headset",
    "Smart Thermostat",
    "Router AX3000",
    "External Monitor 27\"",
    "Studio Microphone",
    "Ring Light",
]

DESCRIPTIONS = [
    "Experience crystal-clear audio with deep bass and long battery life.",
    "Track your health metrics with a bright AMOLED display and GPS.",
    "Tactile switches, RGB lighting, and durable PBT keycaps.",
    "Capture stunning footage with 4K stabilization and waterproof case.",
    "Rich sound in a compact design with 12-hour playtime.",
    "Ultra-fast transfers in a pocket-sized aluminum body.",
    "Immersive sound with ANC and transparency modes.",
    "Ergonomic design with adjustable DPI and programmable buttons.",
    "Expand your ports with HDMI, USB 3.0, and SD card support.",
    "Aluminum build with adjustable height and cable management.",
    "Full HD clarity with noise-reduction microphone.",
    "Adjustable color temperature and USB-powered convenience.",
    "Control your devices remotely with voice assistant integration.",
    "Heart rate, sleep tracking, and water resistance.",
    "Stabilized flight, 2.7K camera, and beginner-friendly controls.",
    "Glare-free screen with weeks-long battery.",
    "Fast wireless charging with temperature control.",
    "High-capacity battery with PD fast charging.",
    "Next-gen immersion with wide FOV and crisp visuals.",
    "Save energy with adaptive scheduling and remote control.",
    "Wi‑Fi 6 speeds with MU‑MIMO and WPA3 security.",
    "IPS panel, 1440p resolution, and slim bezels.",
    "Broadcast-quality audio with cardioid pickup pattern.",
    "Even lighting for video calls and content creation.",
]


class Command(BaseCommand):
    help = "Seed the database with dummy products"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=24, help='Number of products to create')
        parser.add_argument('--flush', action='store_true', help='Delete existing products before seeding')

    def handle(self, *args, **options):
        count = options['count']
        if options['flush']:
            Product.objects.all().delete()
            self.stdout.write(self.style.WARNING('Deleted existing products'))

        created = 0
        for i in range(count):
            name = NAMES[i % len(NAMES)]
            description = DESCRIPTIONS[i % len(DESCRIPTIONS)]
            price = Decimal(random.randint(20, 300)) + Decimal(random.choice([0, 0.49, 0.99]))
            stock_quantity = random.randint(0, 120)

            product = Product(
                name=f"{name} #{i+1}",
                description=description,
                price=price,
                in_stock=stock_quantity > 0,
                stock_quantity=stock_quantity,
            )
            # code auto-generated in model save()
            product.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} products"))


