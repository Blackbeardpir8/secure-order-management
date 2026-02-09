import uuid6
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import UserManager  # Make sure managers.py is in the same folder

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"

    # ✅ FIXED: Use 'id' only. 
    # UUIDv7 is used for security + DB performance.
    id = models.UUIDField(primary_key=True, default=uuid6.uuid7, editable=False)

    # db_index=True makes looking up users by email much faster
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=10,choices=Role.choices,default=Role.USER,)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Link the custom manager
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] # Email is handled by USERNAME_FIELD

    def __str__(self) -> str:
        return self.email
    
    def save(self, *args, **kwargs):
        """
        Overriding the save method ensures that:
        1. Email is always lowercase (Normalization).
        2. We don't rely solely on the frontend or manager to fix data.
        """
        if self.email:
            self.email = self.email.lower().strip()  # Lowercase + Remove spaces
        
        super().save(*args, **kwargs)
