from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from circle.models import Member, Alien
import uuid

ETHERPAD_BASE_URL = "https://pad.c-base.org/p/circle"


class Circle(models.Model):
    class Meta:
        ordering = ['date']

    # The circle takes place on a specific date.
    # There is only one circle on that date
    # The date of the circle is set when the circle is formally opened.
    date = models.DateField(unique=True, db_index=True, null=True, blank=True)

    # A circle is formally opened and closed by timestamp.
    opened = models.DateTimeField(null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)

    # There are several different kinds of attendees to a circle. They are
    # divided into their individual roles they have during the circle.
    # These attributes usually won't be given when creating this model, but
    # will rather be stacked as soon as the circle starts to begin.
    attending_circle_members = models.ManyToManyField(Member, null=True, blank=True,
                                                      related_name='circles_where_circle_member')
    attending_board_members = models.ManyToManyField(Member, null=True, blank=True,
                                                     related_name='circles_where_board_member')
    attending_regular_members = models.ManyToManyField(Member, null=True, blank=True,
                                                       related_name='circles_where_regular_member')
    attending_aliens = models.ManyToManyField(Alien, null=True, blank=True,
                                              related_name='circles_where_alien')

    # Every circle has a designated moderator. The moderated is informally
    # elected during the buildup-phase of the circle and must not be present
    # when creating the model. The moderator's purpose is to moderate the real
    # people, as well as formally opening/closing the circle.
    moderator = models.ForeignKey(Member, related_name='moderated_circles', null=True, blank=True)

    # Every circle has at least one transcript writer who is also informally
    # elected during buildup-phase and must not be present when creating the
    # model. It's the transcript writer's duty to force the meeting into the
    # the protocol, opening/closing of topics, writing the voting/poll
    # texts and maintaining the word-list.
    transcript_writers = models.ManyToManyField(Member, related_name='transcript_circles', null=True, blank=True)

    def __str__(self):
        return "Circle-{}".format(self.date.strftime("%Y-%m-%d"))

    @classmethod
    def create(cls, *args, **kwargs):
        """Overwrite model creation.

        When a new circle instance is created, automatically attach all
        detached topics.
        """
        circle = cls(*args, **kwargs)
        topics = Topic.objects.filter(circle=None)
        for topic in topics:
            topic.circle = circle
            topic.save()
        return circle

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
    def locked(self):
        """Check if this circle is closed."""
        return bool(self.opened and self.closed)

    @staticmethod
    def get_or_create_circle():
        """Wrapper for getting or creating a new circle."""
        try:
            circle = Circle.objects.get(date=None)
        except Circle.DoesNotExist:
            circle = Circle()
            circle.save()
        return circle

    @property
    def is_clear_for_formal_opening(self):
        """Check if this circle is clear for formal opening."""
        if not self.opened:
            if len(self.attending_circle_members.all()) >= 5:
                if len(self.transcript_writers.all()) > 0:
                    if self.moderator:
                        return True
        return False

    @property
    def is_clear_for_formal_closing(self):
        """Check if this circle is clear for formal closing."""
        if self.opened:
            if not self.closed:
                if reduce(lambda x, y: x == y, [True, True] + [bool(t.closed) for t in self.topics.all()]):
                    return True
        return False

    def open_circle(self, force=False):
        """Formally open the circle meeting."""
        if force is not True:
            if not self.is_clear_for_formal_opening:
                raise ValidationError("Not ready for formal opening!")

        timestamp = timezone.now()
        self.opened = timestamp
        self.date = timestamp.date()
        self.save()

    def close_circle(self):
        """Formally close the circle meeting."""
        timestamp = timezone.now()
        self.closed = timestamp
        self.save()
        return self.get_or_create_circle()

    def save(self, *args, **kwargs):
        """Overwrite model save method.

        Field validation is enforced on every save.
        """
        self.clean_fields()
        return super(Circle, self).save(*args, **kwargs)


class Topic(models.Model):
    class Meta:
        unique_together = ['circle', 'headline']
        ordering = ['created', 'headline']

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
        return cls(
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
