from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class MyAccountManager(BaseUserManager):
    def create_user(self, username, password=None
                    ):
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=str(username).lower(),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, Email_Address, password):
    #     user = self.create_user(
    #         Email_Address=self.normalize_email(Email_Address),
    #         password=password,
    #     )
    #     user.is_admin = Trues
    #     user.is_active = True
    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.save(using=self._db)


class User(AbstractBaseUser):
    # Email_Address = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True, null=True,
    #                                   default=None)
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'

    objects = MyAccountManager()

    class Meta:
        db_table = "tbl_users"

    # def __str__(self):
    #     return str(self.username)
    #
    # def has_perm(self, perm, obj=None): return self.is_superuser
    #
    # def has_module_perms(self, app_label): return self.is_superuser
