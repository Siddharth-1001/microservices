import hashlib
from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core import validators
from django.db import models

from .constant import BLOOD_GROUP_CHOICES, GENDER_CHOICES


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, first_name, last_name, phone_number, password=None, password1=None
    ):
        """
        Creates and saves a User with the given email, first_name, last_name, phone_number and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, phone_number, password=None
    ):
        """
        Creates and saves a superuser with the given email, first_name, last_name, phone_number and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=30, null=True, blank=True)
    user_hash = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r"^\d{7,10}$", message="Enter a valid phone number."
            )
        ],
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(
        max_length=1, choices=BLOOD_GROUP_CHOICES, blank=True, null=True
    )
    parents = models.ManyToManyField("CustomUser", blank=True, related_name="children")
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    def save(self, *args, **kwargs):
        if not self.user_hash:
            # Generate a user hash based on the email address
            self.user_hash = hashlib.sha256(self.email.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Check if the user has the specific permission
        # For example, "can_view_dashboard"
        return self.is_admin or self.is_superuser or super().has_perm(perm)

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Check if the user has any permissions for the given app_label
        return (
            self.is_admin
            or self.is_superuser
            or self.user_permissions.filter(content_type__app_label=app_label).exists()
        )
