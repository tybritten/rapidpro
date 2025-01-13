from django.contrib.gis.geos.collections import MultiPolygon
from django.core.management import call_command

from temba.locations.models import AdminBoundary
from temba.tests import MigrationTest


class PopulateLocationsTest(MigrationTest):
    app = "locations"
    migrate_from = "0033_adminboundary_geometry"
    migrate_to = "0034_populate_json_geometry"

    def setUpBeforeMigration(self, apps):
        self.assertEqual(0, AdminBoundary.objects.all().count())
        call_command("import_geojson", "test-data/rwanda.zip")
        self.assertEqual(9, AdminBoundary.objects.all().count())

        self.country = AdminBoundary.objects.get(level=0)
        self.assertIsInstance(self.country.simplified_geometry, MultiPolygon)
        self.assertIsInstance(self.country.simplified_geometry.geojson, str)
        self.assertIsNone(self.country.geometry)

    def test_migrations(self):
        self.assertEqual(9, AdminBoundary.objects.all().count())
        self.country.refresh_from_db()
        self.assertIsInstance(self.country.geometry, dict)
