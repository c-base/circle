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
    email = models.EmailField(blank=True, db_index=True)

    USERNAME_FIELD = 'crew_name'

    def __str__(self):
        return self.crew_name


