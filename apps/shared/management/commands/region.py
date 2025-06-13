import csv
import os

from django.conf import settings
from django.core.management import base

from apps.users.models.locations import Region


class Command(base.BaseCommand):
    help = "Import CSV data into Region model"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_path",
            nargs="?",
            default=os.path.join(
                settings.BASE_DIR, "assets/resources/regions.csv"
            ),
        )

    def handle(self, *args, **options):
        csv_path = options.get("csv_path")

        if not os.path.exists(csv_path):
            self.stdout.write(
                self.style.ERROR(f"CSV file not found at {csv_path}")
            )
            return

        try:
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                # Check for BOM and remove it if present
                first_char = csvfile.read(1)
                if first_char != "\ufeff":
                    csvfile.seek(0)

                reader = csv.DictReader(csvfile)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"ID {Region._meta.verbose_name_plural} imported"
                    )
                )
                for row in reader:
                    region_id = row.get("id", None)
                    region_uz = row.get("name_uz", None)
                    region_ru = row.get("name_ru", None)
                    region_ko = row.get("name_oz", None)
                    soato_id = row.get("soato_id", None)
                    self.stdout.write(self.style.SUCCESS(f"ID {region_id}"))

                    if not region_id:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Skipping row with missing id: {row}"
                            )
                        )
                        continue

                    try:
                        region = Region.objects.get(id=region_id)
                        if region_uz:
                            region.name_uz = region_uz
                        if region_ru:
                            region.name_ru = region_ru
                        if region_ko:
                            region.name_ko = region_ko
                        if soato_id:
                            region.soato_id = soato_id
                        region.save()
                        self.stdout.write(
                            self.style.SUCCESS(f"Region updated: {row}")
                        )
                    except Region.DoesNotExist:
                        Region.objects.create(
                            id=region_id,
                            name_uz=region_uz,
                            name_ru=region_ru,
                            name_ko=region_ko,
                            soato_id=soato_id,
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f"Region created: {row}")
                        )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
