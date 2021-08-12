from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)
    address = models.CharField(max_length=70, null=True, blank=True)
    verification_code = models.IntegerField(default=19563)
    verified = models.BooleanField(default=False)
    emailVerified = models.BooleanField(default=False)
    avatar = models.ImageField('group picture', upload_to="avatars/", default='admin.png')


class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['user', 'friend'], name="unique_friends")
    #     ]


class ExpenseGroup(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, through='Membership')
    avatar = models.ImageField('group picture', upload_to="avatars/", default='admin.png')

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person")
    group = models.ForeignKey(ExpenseGroup, on_delete=models.CASCADE, related_name="group")
    date_joined = models.DateField(default=timezone.now)
