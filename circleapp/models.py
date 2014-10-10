from django.db import models
from django.utils import timezone
from circle.models import Member, Alien
from hashlib import md5
import datetime

ETHERPAD_BASE_URL = "https://pad.c-base.org/p/circle"


class Circle(models.Model):
    class Meta:
        ordering = ['date']

    # The circle takes place on a specific date.
    # There is only one circle on that date
    # The date of the circle is set when the circle is formally opened.
    date = models.DateField(unique=True, db_index=True)

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
        return bool(not self.opened and not self.closed)

    @property
    def ongoing(self):
        """Is this circle currently ongoing?"""
        return bool(self.opened and not self.closed)

    @property
    def locked(self):
        return bool(self.opened and self.closed)

    def is_clear_for_formal_opening(self):
        """Return boolean if this circle is clear for formal opening."""
        if not self.opened:
            if len(self.attending_circle_members.all()) >= 5:
                if len(self.transcript_writers.all()) > 0:
                    if self.moderator:
                        return True
        return False

    def is_clean_for_formal_closing(self):
        if self.opened:
            if not self.closed:
                if reduce(lambda x, y: x == y, [bool(t.closed) for t in self.topics.all()]):
                    return True
        return False

    def open_circle(self):
        """Formally open the circle meeting."""
        timestamp = timezone.now()
        self.opened = timestamp
        self.date = timestamp.date()
        self.save()

    def close_circle(self):
        """Formally close the circle meeting."""
        timestamp = timezone.now()
        self.closed = timestamp
        self.save()


class Topic(models.Model):
    class Meta:
        unique_together = ['circle', 'headline']
        ordering = ['order', 'headline']

    # A topic is always linked to a circle...
    circle = models.ForeignKey(Circle, related_name='topics')

    # ... an ordering attribute...
    order = models.IntegerField(default=0)

    # ... an applicant ...
    applicant = models.CharField(max_length=64)

    # ... and a main headline.
    headline = models.CharField(max_length=128, db_index=True)

    # Some topics have a god-father member which we'll call the sponsor.
    sponsor = models.ForeignKey(Member, related_name='topic_sponsorship')

    # Here we store the URL of the etherpad to this topic.
    # baccenfutter: I choose CharField over URLField, because I was afraid the
    # latter would possible bring limitations we don't want to tackle with.
    etherpad = models.CharField(max_length=256, editable=False)     # Auto-set during validation.

    # A topic is formally opened and closed.
    opened = models.DateTimeField(null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.headline

    @property
    def upcoming(self):
        return bool(not self.opened and not self.closed)

    @property
    def ongoing(self):
        return bool(self.opened and not self.closed)

    @property
    def locked(self):
        return bool(self.opened and self.closed)

    @property
    def etherpad_link(self):
        """Generate and return the etherpad link to this topic."""
        base_url = "https://pad.c-base.org/p/"
        return "{}circle-{}/topic-{}".format(
            base_url,
            self.circle.name,
            md5(self.headline).hexdigest()
        )


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
