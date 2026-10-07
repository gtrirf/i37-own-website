from django.apps import apps
from django.core.management.base import BaseCommand

from apps.images import convert_existing_images


class Command(BaseCommand):
    help = "Bazadagi mavjud rasmlarni (ImageField + CKEditor blog rasmlari) WebP formatiga o'tkazadi."

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-originals', action='store_true',
            help="O'tkazilgandan keyin eski (png/jpg) fayllarni o'chirish",
        )

    def handle(self, *args, **options):
        converted, originals = convert_existing_images(
            apps, delete_originals=options['delete_originals'], log=self.stdout.write
        )
        self.stdout.write(self.style.SUCCESS(f'Tayyor: {converted} ta yozuv yangilandi, {len(originals)} ta fayl WebP ga o\'tkazildi.'))
