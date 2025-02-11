from django.contrib.auth import get_user_model

from temba.tests import TembaTest


class UserTest(TembaTest):
    def test_user_model(self):
        long_username = "bob12345678901234567890123456789012345678901234567890@msn.com"
        get_user_model().objects.create(username=long_username, email=long_username)
