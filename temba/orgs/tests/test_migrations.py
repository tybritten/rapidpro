from temba.tests import MigrationTest


class RemoveViewersTest(MigrationTest):
    app = "orgs"
    migrate_from = "0163_squashed"
    migrate_to = "0164_remove_viewers"

    def test_migration(self):
        self.assertEqual({self.admin, self.editor, self.agent}, set(self.org.get_users()))
