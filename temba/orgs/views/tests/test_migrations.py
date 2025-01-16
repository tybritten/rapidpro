from temba.tests import MigrationTest


class GrantPrometheusFeatureTest(MigrationTest):
    app = "orgs"
    migrate_from = "0164_remove_viewers"
    migrate_to = "0165_grant_prometheus_feature"

    def setUpBeforeMigration(self, apps):
        self.org.prometheus_token = "sesame"
        self.org.save(update_fields=("prometheus_token",))

    def test_migration(self):
        self.org.refresh_from_db()
        self.org2.refresh_from_db()

        self.assertIn("prometheus", self.org.features)
        self.assertNotIn("prometheus", self.org2.features)
