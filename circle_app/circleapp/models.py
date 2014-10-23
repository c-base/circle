from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from circle.models import Member, Alien
import uuid
from managers import CircleManager, TopicManager

ETHERPAD_BASE_URL = "https://pad.c-base.org/p/circle"
CIRCLE_ROLES = (
    ('writer', 'Transcript Writer'),
    ('mod', 'Moderator')
)
POLL_OUTCOMES = (
    (0, 'Negative'),
    (1, 'Positive'),
    (2, 'Neutral'),
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

    objects = CircleManager()

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

    def open(self):
        """Formally open the circle session."""
        self.date = timezone.now().date()
        self.opened = timezone.now()
        self.save()
        Circle().save()
        return self

    def close(self):
        """Formally close the circle session."""
        self.closed = timezone.now()
        return self


class Participant(models.Model):
    circle = models.ForeignKey(Circle, related_name='participants')
    member = models.ForeignKey(Member, related_name='participations')
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    # Participants may have a special role assigned to them.
    role = models.CharField(max_length=16, choices=CIRCLE_ROLES, null=True, blank=True, default="")

    def __repr__(self):
        return "{} -> {}".format(self.member.crew_name, self.circle.date or "Upcoming...")


class Guest(models.Model):
    circle = models.ForeignKey(Circle, related_name='guests')
    alien = models.ForeignKey(Alien, related_name='participations')
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    def __repr__(self):
        return "{} {} -> {}".format(self.alien.first_name, self.alien.last_name, self.circle.date)


class Topic(models.Model):
    class Meta:
        unique_together = ['circle', 'headline']
        ordering = ['-created', 'headline']

    # A topic is linked to a circle...
    circle = models.ForeignKey(Circle, related_name='topics')

    # ... an applicant ...
    applicant_member = models.ForeignKey(Member, related_name='topic_applications', null=True, blank=True)
    applicant_alien = models.ForeignKey(Alien, related_name='topic_applications', null=True, blank=True)

    # ... a creation timestamp ...
    created = models.DateTimeField(auto_now_add=True)

    # ... and a headline.
    headline = models.CharField(max_length=128, db_index=True)

    # Some topics have a god-father member which we'll call the sponsor.
    sponsor = models.ForeignKey(Member, related_name='topic_sponsorships', null=True, blank=True)

    # A topic is formally opened and closed.
    opened = models.DateTimeField(null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)

    # Each topic also has a unique identifier. This comes in handy in several
    # use-cases, such as the pad-url.
    uuid = models.CharField(max_length=36, unique=True)

    objects = TopicManager()

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

    def open_topic(self):
        """Formally open this topic."""
        timestamp = timezone.now()
        self.opened = timestamp
        self.save()
        return self

    def close_topic(self):
        """Formally close this topic."""
        timestamp = timezone.now()
        self.closed = timestamp
        self.save()
        return self


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
    outcome = models.CharField(max_length=8, choices=POLL_OUTCOMES)

    def __str__(self):
        return self.proposal

    @classmethod
    def create(cls, topic, proposal):
        return cls(
            topic=topic,
            proposal=proposal,
        )
