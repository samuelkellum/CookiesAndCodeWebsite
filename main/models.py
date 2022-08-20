from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

EVENT_POINTS = 10 # points attained for attending an event
MEETING_POINTS = 5 # points attained for attending a meeting


class CustomUser(AbstractBaseUser, PermissionsMixin):

    TIER_STANDARDS = {
        'Platinum': 100,
        'Gold': 80,
        'Silver': 60,
        'Bronze': 40

    } # changem123890

    email = models.EmailField(_('email address'), unique=True)
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    is_eboard = models.BooleanField(default=False)

    POSITION_CHOICES = [

        ('P', 'President'),
        ('VP', 'Vice President'),
        ('VPA', 'Vice President of Administration'),
        ('VPF', 'Vice President of Finance')

    ]

    position = models.CharField(max_length=30, choices=POSITION_CHOICES, blank=True, null=True)

 
    membership_points = models.IntegerField(default=0) # total membership points for member

    TIER_CHOICES = [

        ('P', 'Platinum'),
        ('G', 'Gold'),
        ('S', 'Silver'),
        ('B', 'Bronze'),
        ('N', 'None')
    ]

    membership_tier = models.CharField(max_length=12, choices=TIER_CHOICES, default='N', blank=True, null=True)

    YEAR_IN_SCHOOL_CHOICES = [
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
    ]

    year_in_school = models.CharField(max_length=12, choices=YEAR_IN_SCHOOL_CHOICES, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def add_points_update_membership_tier(self, points):
        self.membership_points += points

        if self.membership_points >= TIER_STANDARDS['Platinum']:
            self.membership_tier = 'P'

        elif self.membership_points >= TIER_STANDARDS['Gold']:
            self.membership_tier = 'G'

        elif self.membership_points >= TIER_STANDARDS['Silver']:
            self.membership_tier = 'S'

        elif self.membership_points >= TIER_STANDARDS['Bronze']:
            self.membership_tier = 'B'

        else:
            self.membership_tier = 'N'




class Event(models.Model):
    ''' Model to represent our events '''

    name = models.CharField(max_length=100)
    organizers = models.ManyToManyField(CustomUser, related_name='event_organizers', related_query_name='event_organizers')
    date_time = models.DateTimeField()
    location = models.CharField(max_length=100) # room number
    attendees = models.ManyToManyField(CustomUser)
    points = models.IntegerField(default=EVENT_POINTS)


class Meeting(models.Model):
    ''' Model to represent our weekly meetings '''
    date_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    attendees = models.ManyToManyField(CustomUser)
    points = models.IntegerField(default=MEETING_POINTS)

