from django.utils import timezone

from temba.tests import MigrationTest


class BackfillNewUserFieldsTest(MigrationTest):
    app = "users"
    migrate_from = "0006_add_new_user_fields"
    migrate_to = "0007_backfill_new_user_fields"

    def setUpBeforeMigration(self, apps):
        self.editor.language = "fr"
        self.editor.last_auth_on = timezone.now()
        self.editor.avatar = "http://face.jpg"
        self.editor.is_system = True
        self.editor.two_factor_enabled = True
        self.editor.two_factor_secret = "2345"
        self.editor.email_status = "V"
        self.editor.email_verification_secret = "sesame"
        self.editor.external_id = "34567"
        self.editor.verification_token = "987654"
        self.editor.save()

    def test_migration(self):
        self.editor.refresh_from_db()
        self.assertEqual(self.editor.language, self.editor.settings.language)
        self.assertEqual(self.editor.last_auth_on, self.editor.settings.last_auth_on)
        self.assertEqual(self.editor.avatar, self.editor.settings.avatar)
        self.assertEqual(self.editor.is_system, self.editor.settings.is_system)
        self.assertEqual(self.editor.two_factor_enabled, self.editor.settings.two_factor_enabled)
        self.assertEqual(self.editor.two_factor_secret, self.editor.settings.otp_secret)
        self.assertEqual(self.editor.email_status, self.editor.settings.email_status)
        self.assertEqual(self.editor.email_verification_secret, self.editor.settings.email_verification_secret)
        self.assertEqual(self.editor.external_id, self.editor.settings.external_id)
        self.assertEqual(self.editor.verification_token, self.editor.settings.verification_token)
