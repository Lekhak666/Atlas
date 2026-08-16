from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class AtlasUserManager(UserManager):
    """
    Custom manager for the Atlas User model.

    Email is the authentication identity.
    Username remains a required public handle.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The email address must be provided.")

        if not username:
            raise ValueError("The username must be provided.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email,
        username,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )


class User(AbstractUser):
    """
    Atlas user identity.

    Email is the authentication identity.
    Username is the public handle.
    """

    email = models.EmailField(
        unique=True,
    )

    avatar = models.URLField(
        blank=True,
    )

    bio = models.TextField(
        blank=True,
    )

    timezone = models.CharField(
        max_length=64,
        default="Asia/Kolkata",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = AtlasUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email