import csv
import os

from django.conf import settings
from django.core.management import base

from apps.users.models.locations import Region, District


class Command(base.BaseCommand):
    help = "Import district data from CSV"

    def handle(self, *args, **options):
        csv_path = os.path.join(settings.BASE_DIR, "assets/resources/districts.csv")
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found at {csv_path}"))
            return

        try:
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                first_char = csvfile.read(1)
                if first_char != "\ufeff":
                    csvfile.seek(0)
                reader = csv.DictReader(csvfile)
                for row in reader:
                    district_id = row.get("id")
                    region_id = row.get("region_id", None)
                    district_uz = row.get("name_uz", None)
                    district_ru = row.get("name_ru", None)
                    district_ko = row.get("name_oz", None)
                    soato_id = row.get("soato_id", None)

                    if not district_id or not region_id:
                        self.stdout.write(
                            self.style.ERROR(f"Skipping row with missing data: {row}")
                        )
                        continue

                    try:
                        region = Region.objects.filter(id=int(region_id)).first()
                        if not region:
                            self.stdout.write(
                                self.style.ERROR(
                                    f"Region with id {region_id} does not exist"
                                )
                            )
                            continue

                        district, created = District.objects.update_or_create(
                            id=district_id,
                            defaults={
                                "region": region,
                                "name_uz": district_uz,
                                "name_ru": district_ru,
                                "name_ko": district_ko,
                                "soato_id": soato_id,
                            },
                        )

                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(f"District {district_uz} added")
                            )
                        else:
                            self.stdout.write(
                                self.style.SUCCESS(f"District {district_uz} updated")
                            )

                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"Error while processing row {row}: {e}")
                        )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
