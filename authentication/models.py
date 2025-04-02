from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django_countries import countries


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    artist_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    ROLES = (
        ('user', 'Regular User'),
        ('artist', 'Artist'),
        ('venue_owner', 'Venue Owner'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=15, choices=ROLES, default='user')
    last_login = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    state = models.CharField(max_length=15)
    city = models.CharField(max_length=25)
    country = models.CharField(max_length=100, null=True, blank=True, choices=countries)
    phone_regex = RegexValidator(regex=r'^\+?234?\d{9,15}$', message="Phone number must be entered in the format: "
                                                                     "'+2348031234567'.")
    telephone = models.CharField(max_length=15, validators=[phone_regex])
    is_staff = models.BooleanField(default=False)

    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['telephone']

    def __str__(self):
        return self.email
