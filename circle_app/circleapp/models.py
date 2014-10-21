from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from circle.models import Member, Alien
import uuid

ETHERPAD_BASE_URL = "https://pad.c-base.org/p/circle"
CIRCLE_ROLES = (
    ('participant', 'Participant'),
    ('writer', 'Transcript Writer'),
    ('mod', 'Moderator')
)


class Circle(models.Model):
    class Meta:
        ordering = ['-date']

    # The circle takes place on a specific date.
    # There is only one circle on that date
    # The date of the circle is set when the circle is formally opened.
    date = models.DateField(unique=True, db_index=True, null=True, blank=True)

    # A circle is formally opened and closed by timestamp.
    opened = models.DateTimeField(null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.date:
            return "Circle-{}".format(self.date.strftime("%Y-%m-%d"))
        else:
            return "Upcoming..."

    @property
    def name(self):
        return self.date.strftime('%Y-%m-%d')

    @property
    def upcoming(self):
        """Check if this circle is still upcoming."""
        return bool(not self.opened and not self.closed)

    @property
    def ongoing(self):
        """Is this circle currently ongoing?"""
        return bool(self.opened and not self.closed)

    @property
    def over(self):
        """Check if this circle is closed."""
        return bool(self.opened and self.closed)


class Participant(models.Model):
    circle = models.ForeignKey(Circle, related_name='participants')
    member = models.ForeignKey(Member, related_name='participations')
    role = models.CharField(max_length=16, choices=CIRCLE_ROLES, default='participant')
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField()

    def __repr__(self):
        return "{} -> {}".format(self.member.crew_name, self.circle.date)


class Guest(models.Model):
    circle = models.ForeignKey(Circle, related_name='guests')
    alien = models.ForeignKey(Alien, related_name='participations')
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField()

    def __repr__(self):
        return "{} {} -> {}".format(self.alien.first_name, self.alien.last_name, self.circle.date)


class Topic(models.Model):
    class Meta:
        unique_together = ['circle', 'headline']
        ordering = ['-created', 'headline']

    # A topic is linked to a circle...
    circle = models.ForeignKey(Circle, related_name='topics')

    # ... an applicant ...
    applicant = models.CharField(max_length=64)

    # ... a creation timestamp ...
    created = models.DateTimeField(auto_now_add=True)

    # ... and a headline.
    headline = models.CharField(max_length=128, db_index=True)

    # Some topics have a god-father member which we'll call the sponsor.
    sponsor = models.ForeignKey(Member, related_name='topic_sponsorship', null=True, blank=True)

    # A topic is formally opened and closed.
    opened = models.DateTimeField(null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)

    # Each topic also has a unique identifier. This comes in handy in several
    # use-cases, such as the pad-url.
    uuid = models.CharField(max_length=36, unique=True)

    @classmethod
    def create(cls, applicant, headline):
        """Create a new topic.

        :param applicant:   object  - Instance of Member model
        :param headline:    str     - Subject of topic
        """
        try:
            circle = [c for c in Circle.objects.all() if c.upcoming][0]
        except IndexError:
            raise IndexError("Can not find any upcoming circle-events!")
        return cls(
            circle=circle,
            applicant=applicant,
            headline=headline,
            uuid=uuid.uuid4(),
        )

    def __str__(self):
        return str(self.uuid)

    @property
    def upcoming(self):
        """Check if this topic is still upcoming."""
        return bool(not self.opened and not self.closed)

    @property
    def ongoing(self):
        """Check if this circle is currently ongoing."""
        return bool(self.opened and not self.closed)

    @property
    def locked(self):
        """Check if this circle has been closed."""
        return bool(self.opened and self.closed)

    @property
    def etherpad_link(self):
        """Return the etherpad link to this topic."""
        base_url = ETHERPAD_BASE_URL
        return "{}/circle-topic-{}".format(base_url, self.uuid)

    @property
    def is_clear_for_formal_opening(self):
        """Check if topic is clear for formal opening."""
        if self.circle and self.circle.ongoing:
            if not self.opened:
                if not self.closed:
                    # This hack basically checks if all other topics are closed.
                    if not reduce(lambda x, y: x == y, [True, True] + [t.closed for t in self.circle.topics.all()]):
                        return True
        return False

    @property
    def is_clear_for_formal_closing(self):
        """Check if topic is clear for formal closing."""
        if self.opened:
            if not self.closed:
                return True
        return False

    def open_topic(self, force=False):
        """Formally open this topic."""
        if force is not True:
            if not self.is_clear_for_formal_opening:
                raise ValidationError("Not ready for formal opening!")

        timestamp = timezone.now()
        self.opened = timestamp
        self.save()
        return self

    def close_topic(self, force=False):
        """Formally close this topic."""
        if force is not True:
            if not self.is_clear_for_formal_closing:
                raise ValidationError("Not ready for formal closing!")

        timestamp = timezone.now()
        self.closed = timestamp
        self.save()
        return self

    def save(self, *args, **kwargs):
        """Overwrite model save method.

        Force field validation on every save.
        """
        self.clean_fields()
        return super(Topic, self).save(*args, **kwargs)


class Voting(models.Model):
    # A voting is always connected to one and only one topic...
    topic = models.OneToOneField(Topic, related_name='voting')

    # ... has a formal proposal...
    proposal = models.CharField(max_length=1024, db_index=True)

    # ... and a number of votes.
    positive = models.IntegerField()
    negative = models.IntegerField()
    abstentions = models.IntegerField()

    def __str__(self):
        return self.proposal

    @classmethod
    def create(cls, topic, proposal):
        return cls(
            topic=topic,
            proposal=proposal,
        )

    @property
    def is_valid(self):
        total_votes = self.positive + self.negative + self.abstentions
        if total_votes == len(self.topic.circle.attending_circle_members.all()):
            return True

        return False


class Poll(models.Model):
    # A poll is always connected to one and only one topic...
    topic = models.OneToOneField(Topic, related_name='polls')

    # ... has a formal proposal...
    proposal = models.CharField(max_length=1024, db_index=True)

    # ... and an outcome.
    outcome_choices = (
        (0, 'Neutral'),
        (1, 'Positive'),
        (2, 'Negative'),
    )
    outcome = models.CharField(max_length=8, choices=outcome_choices)

    def __str__(self):
        return self.proposal

    @classmethod
    def create(cls, topic, proposal):
        return cls(
            topic=topic,
            proposal=proposal,
        )
