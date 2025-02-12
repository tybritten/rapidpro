import pyotp

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from temba.utils.text import generate_token
from temba.utils.uuid import uuid4


class RecoveryToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="recovery_tokens")
    token = models.CharField(max_length=32, unique=True)
    created_on = models.DateTimeField(default=timezone.now)


class FailedLogin(models.Model):
    username = models.CharField(max_length=256)
    failed_on = models.DateTimeField(default=timezone.now)


class BackupToken(models.Model):
    """
    A 2FA backup token for a user
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="backup_tokens", on_delete=models.PROTECT)
    token = models.CharField(max_length=18, unique=True, default=generate_token)
    is_used = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    @classmethod
    def generate_for_user(cls, user, count: int = 10):
        # delete any existing tokens for this user
        user.backup_tokens.all().delete()

        return [cls.objects.create(user=user) for i in range(count)]

    def __str__(self):
        return self.token


class User(AbstractUser):
    SYSTEM_USER_USERNAME = "system"

    @classmethod
    def create(cls, email: str, first_name: str, last_name: str, password: str, language: str = None):
        assert not cls.get_by_email(email), "user with this email already exists"

        obj = cls.objects.create_user(
            username=email, email=email, first_name=first_name, last_name=last_name, password=password
        )
        if language:
            obj.settings.language = language
            obj.settings.save(update_fields=("language",))
        return obj

    @classmethod
    def get_or_create(cls, email: str, first_name: str, last_name: str, password: str, language: str = None):
        obj = cls.get_by_email(email)
        if obj:
            obj.first_name = first_name
            obj.last_name = last_name
            obj.save(update_fields=("first_name", "last_name"))
            return obj

        return cls.create(email, first_name, last_name, password=password, language=language)

    @classmethod
    def get_by_email(cls, email: str):
        return cls.objects.filter(username__iexact=email).first()

    @classmethod
    def get_orgs_for_request(cls, request):
        """
        Gets the orgs that the logged in user has a membership of.
        """

        return request.user.orgs.filter(is_active=True).order_by("name")

    @classmethod
    def get_system_user(cls):
        user = cls.objects.filter(username=cls.SYSTEM_USER_USERNAME).first()
        if not user:
            user = cls.objects.create_user(cls.SYSTEM_USER_USERNAME, first_name="System", last_name="Update")
        return user

    @property
    def name(self) -> str:
        return self.get_full_name()

    def get_orgs(self):
        return self.orgs.filter(is_active=True).order_by("name")

    def get_owned_orgs(self):
        """
        Gets the orgs where this user is the only user.
        """
        owned_orgs = []
        for org in self.get_orgs():
            if not org.users.exclude(id=self.id).exists():
                owned_orgs.append(org)
        return owned_orgs

    def record_auth(self):
        """
        Records that this user authenticated
        """
        self.settings.last_auth_on = timezone.now()
        self.settings.save(update_fields=("last_auth_on",))

    def enable_2fa(self):
        """
        Enables 2FA for this user
        """

        self.settings.two_factor_enabled = True
        self.settings.save(update_fields=("two_factor_enabled",))

        BackupToken.generate_for_user(self)

    def disable_2fa(self):
        """
        Disables 2FA for this user
        """
        self.settings.two_factor_enabled = False
        self.settings.save(update_fields=("two_factor_enabled",))

        self.backup_tokens.all().delete()

    def verify_2fa(self, *, otp: str = None, backup_token: str = None) -> bool:
        """
        Verifies a user using a 2FA mechanism (OTP or backup token)
        """
        if otp:
            secret = self.settings.otp_secret
            return pyotp.TOTP(secret).verify(otp, valid_window=2)
        elif backup_token:
            token = self.backup_tokens.filter(token=backup_token, is_used=False).first()
            if token:
                token.is_used = True
                token.save(update_fields=("is_used",))
                return True

        return False

    @cached_property
    def is_alpha(self) -> bool:
        return self.groups.filter(name="Alpha").exists()

    @cached_property
    def is_beta(self) -> bool:
        return self.groups.filter(name="Beta").exists()

    def has_org_perm(self, org, permission: str) -> bool:
        """
        Determines if a user has the given permission in the given org.
        """

        # has it innately? e.g. Granter group
        if self.has_perm(permission):
            return True

        role = org.get_user_role(self)
        if not role:
            return False

        return role.has_perm(permission)

    def get_api_tokens(self, org):
        """
        Gets this users active API tokens for the given org
        """
        return self.api_tokens.filter(org=org, is_active=True)

    def as_engine_ref(self) -> dict:
        return {"email": self.email, "name": self.name}

    def release(self, user):
        """
        Releases this user, and any orgs of which they are the sole owner.
        """
        user_uuid = str(uuid4())
        self.first_name = ""
        self.last_name = ""
        self.email = f"{user_uuid}@rapidpro.io"
        self.username = f"{user_uuid}@rapidpro.io"
        self.password = ""
        self.is_active = False
        self.save()

        # release any API tokens
        self.api_tokens.update(is_active=False)

        # release any orgs we own
        for org in self.get_owned_orgs():
            org.release(user, release_users=False)

        # remove user from all roles on other orgs
        for org in self.get_orgs():
            org.remove_user(self)

    def __str__(self):
        return self.name or self.username
