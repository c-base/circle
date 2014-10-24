from django.contrib.auth.models import AbstractBaseUser
from django.db import models

ALIEN_COMPATIBILITY_CHOICES = (
    ('dunno', 'The general compatibility of this alien is undecided.'),
    ('compat', 'This alien is generally compatible.'),
    ('incomp', 'This alien has seemed generally incompatible.'),
)


class Member(AbstractBaseUser):
    crew_name = models.CharField(max_length=256, unique=True, db_index=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True, db_index=True, unique=True)

    USERNAME_FIELD = 'crew_name'

    def __str__(self):
        return self.crew_name


class Alien(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='Given-name')
    last_name = models.CharField(max_length=64, verbose_name='Sir-name', null=True, blank=True)
    organization = models.CharField(max_length=256, null=True, blank=True)
    compatibility = models.CharField(max_length=8, choices=ALIEN_COMPATIBILITY_CHOICES, default='dunno')
    email = models.EmailField(blank=True, db_index=True, unique=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name.capitalize(), self.last_name.capitalize())
        else:
            return self.first_name.capitalize()
