from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_user(self, member_id, name=None, age=None, gender=None, registration_date=None, phone_number=None,
                    athletic_experience=None, expiration_date=None, password=None):
        if not member_id:
            raise ValueError('Users must have an member_id.')

        user = self.model(
            member_id=member_id,
        )
        if name:
            user.name=name
        if age:
            user.age=age
        if gender:
            user.gender=gender
        if registration_date:
            user.registration_date=registration_date
        if phone_number:
            user.phone_number=phone_number
        if athletic_experience:
            user.athletic_experience=athletic_experience
        if expiration_date:
            user.expiration_date=expiration_date

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
    # Used Inheritance in this part.
    # Basic 'User' class provided by Django does not have the feature we want(such as name, age, gender, etc.).
    # So we made new class named 'User' which inherited 'AbstractBaseUser' provided by Django.
    # After set this class as 'AUTH_USER_MODEL' at settings.py, now Django makes each user using this class.

    # We declared each variable as 'Field'
    # each Field has type, such as Char, Integer, Date.
    # If we try to input data which is not appropriate with the field, Django denies it.
    # So this 'Field' system provides validation process.
    member_id = models.CharField(
        verbose_name='member_id',
        max_length=4,
        unique=True,
        blank=False,
    )
    name = models.CharField(
        max_length=30,
        default='noname',
    )
    age = models.IntegerField(
        default='20',
    )
    gender = models.CharField(
        max_length=6,
        default='Male',
        choices=(('Male', 'Male'), ('Female', 'Female'))
    )
    registration_date = models.DateField(
        default='2000-01-01',
    )
    phone_number = models.CharField(
        max_length=11,
        default="00000000000"
    )
    athletic_experience = models.TextField(
        default='',
    )
    expiration_date = models.DateField(
        default='2000-01-01',
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

    # Following series of setVar() functions are made to set variables' value indirectly by user.
    # This is a way to implement "Encapsulation"
    # each function gets value which is to be new value for a variable in object.
    # then the function changes the value accordingly.
    # user cannot change the value of variables in objects by themselves.
    # instead, these functions do.
    def setMemberId(self, member_id):
        self.member_id = member_id
        self.save()

    def setName(self, name):
        self.name = name
        self.save()

    def setAge(self, age):
        self.age = age
        self.save()

    def setGender(self, gender):
        self.gender = gender
        self.save()

    def setRegistrationDate(self, registration_date):
        self.registration_date = registration_date
        self.save()

    def setPhoneNumber(self, phone_number):
        self.phone_number = phone_number
        self.save()

    def setAthleticExperience(self, athletic_Experience):
        self.athletic_experience = athletic_Experience
        self.save()

    def setExpirationDate(self, expiration_date):
        self.expiration_date = expiration_date
        self.save()


    @property
    def is_staff(self):
        return self.is_admin
