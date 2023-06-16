from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_user(self, member_id, password=None):
        if not member_id:
            raise ValueError('Users must have an member_id.')

        user = self.model(
            member_id=member_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, member_id, password):
        user = self.create_user(
            member_id,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    member_id = models.CharField(
        verbose_name='member_id',
        max_length=4,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'member_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.member_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin