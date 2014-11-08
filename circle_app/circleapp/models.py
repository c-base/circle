"""Dear Front-End Developer

In this module you'll find all models directly regarding the
circle-session, such as Circle, Topic, Voting, etc.

Also take a look at circleapp.managers for convenience access methods to circle
instances.

Note: There is always one upcoming circle session. When formally opening this
      session a new instance will be created on-the-fly to serve as a
      collection bin for new and postponed topics.
"""
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.contrib.auth.models import User
from managers import CircleManager, TopicManager, ParticipantManager
from utils import UserMonkeyPatcher
import uuid
import requests

CIRCLE_ROLES = (
    ('writer', 'Transcript Writer'),
    ('mod', 'Moderator')
)
POLL_OUTCOMES = (
    (0, 'Negative'),
    (1, 'Positive'),
    (2, 'Neutral'),
)
TOPIC_RELATIONS = (
    (0, 'related to'),
    (1, 'follow-up of'),
    (2, 'blocked by'),
    (3, 'overrules'),
)


def get_etherpad_config():
    """Retrieve etherpad configuration.

    :returns: dict      - {etherpad_key: str, etherpad_url: str}
    """
    try:
        from circle.settings import ETHERPAD_API_KEY
    except ImportError:
        ETHERPAD_API_KEY = ""
        print "WARNING: No etherpad API-Key defined!"

    try:
        from circle.settings import ETHERPAD_BASE_URL
    except ImportError:
        ETHERPAD_BASE_URL = "/"
        print "WARNING: No etherpad base-url defined!"

    try:
        from circle.settings import ETHERPAD_AUTH
    except ImportError:
        ETHERPAD_AUTH = "", ""
        print "WARNING: No etherpad credentials defined!"

    return {
        'etherpad_key': ETHERPAD_API_KEY,
        'etherpad_url': ETHERPAD_BASE_URL,
        'etherpad_auth': ETHERPAD_AUTH,
    }


# Patch the builtin django user model to contain convenience properties.
setattr(User, 'is_alien', UserMonkeyPatcher.is_alien)
setattr(User, 'is_member', UserMonkeyPatcher.is_member)
setattr(User, 'is_circle_member', UserMonkeyPatcher.is_circle_member)
setattr(User, 'is_board_member', UserMonkeyPatcher.is_board_member)


class Circle(models.Model):
    """Representation of a circle."""
    class Meta:
        ordering = ['-date']

    # The circle takes place on a specific date.
    # There is only one circle on that date
    # The date of the circle is set when the circle is formally opened.
    date = models.DateField(unique=True, db_index=True, null=True, blank=True)

    # A circle is formally opened and closed by timestamp.
    opened = models.DateTimeField(null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)

    # Use a custom manager for this model
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
        self.check_in_attendees()
        self.date = timezone.now().date()
        self.opened = timezone.now()
        self.save()

        # Create a new instance to serve as collection bin for topics.
        if not Circle.objects.upcoming():
            Circle().save()

        return self

    def close(self):
        """Formally close the circle session."""
        self.check_out_attendees()
        self.closed = timezone.now()
        return self

    def check_in_attendees(self):
        timestamp = timezone.now()

        for attendee in self.participants.all():
            attendee.check_in == timestamp
            attendee.save()

    def check_out_attendees(self):
        timestamp = timezone.now()

        for attendee in self.participants.all():
            attendee.check_out == timestamp
            attendee.save()


class Participant(models.Model):
    """Representation of a circle-participant.

    A participant is a user-object attending a circle session.
    """

    # A specific user...
    user = models.ForeignKey(User, related_name='participations')

    # ... attends a specific circle session.
    circle = models.ForeignKey(Circle, related_name='participants')

    # Check-in and check-out are formally logged.
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    # Participants may have a special role assigned to them.
    role = models.CharField(max_length=16, choices=CIRCLE_ROLES, null=True, blank=True, default="")

    # Use a custom manager for this model.
    objects = ParticipantManager()

    def __repr__(self):
        return "{} -> {}".format(self.user.username, self.circle.date or "Upcoming...")


class Topic(models.Model):
    """Representation of a topic."""

    class Meta:
        unique_together = ['circle', 'headline']
        ordering = ['created', 'headline']

    # A topic is always linked to a circle. In most cases this will
    # be the next upcoming circle that is ensured to always be
    # present in the database, by the Circle model.
    circle = models.ForeignKey(Circle, related_name='topics')

    # Every topic has an applicant and may have one or more proxies
    # who present the topic to the circle.
    applicant = models.ForeignKey(User, related_name='topic_applications', null=True, blank=True)
    proxy = models.CharField(max_length=256, null=True, blank=True)

    # The creation timestamp of a topic is saved for statistical
    # reasons.
    created = models.DateTimeField(auto_now_add=True)

    # The main body of a topic consists of a headline and a shot
    # summary.
    headline = models.CharField(max_length=128, db_index=True)
    summary = models.TextField()

    # Some topics have a god-father member which we'll call the
    # sponsor. This member acts as communication interface between
    # the circle and the applicant for further actions and
    # coordination.
    sponsor = models.ForeignKey(User, related_name='topic_sponsorships', null=True, blank=True)

    # A topic is formally opened and closed by timestamp.
    opened = models.DateTimeField(null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)

    # Each topic also has a unique identifier. This comes in handy in several
    # use-cases, such as the pad-url.
    uuid = models.CharField(max_length=36, unique=True, db_index=True)

    # When formally closing a topic, the etherpad text is persisted into the
    # database.
    transcript_protocol = models.TextField(editable=False, default="", null=True, blank=True)

    # Use a custom manager for this model.
    objects = TopicManager()

    # Fetch the etherpad config from settings.
    etherpad_config = get_etherpad_config()

    @classmethod
    def create(cls, headline, **kwargs):
        """Create a new topic.

        :param applicant:   object  - Instance of Member model
        :param headline:    str     - Subject of topic
        """
        try:
            circle = [c for c in Circle.objects.all() if c.upcoming][0]
        except IndexError:
            raise IndexError("Can not find any upcoming circle-events!")
        topic = cls(
            circle=circle,
            headline=headline,
            uuid=uuid.uuid4(),
        )
        for key, value in kwargs.iteritems():
            setattr(topic, key, value)
        return topic

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
    def over(self):
        """Check if this circle has been closed."""
        return bool(self.opened and self.closed)

    @property
    def etherpad_id(self):
        return "circle-topic-{}".format(self.uuid)

    @property
    def etherpad_link(self):
        """Return the etherpad link to this topic."""
        base_url = self.etherpad_config['etherpad_url']
        return "{}/p/{}".format(base_url, self.etherpad_id)

    def etherpad_create(self):
        """Make API call to create the pad.

        :raises: ImproperlyConfigured   - If there is a problem communicating
                                          with the pad.
        :raises: RuntimeError           - If pad returns a status-code that is
                                          not zero.
        """
        url = "{}/api/1/createPad?apikey={}&padID={}&text={}".format(
            self.etherpad_config['etherpad_url'],
            self.etherpad_config['etherpad_key'],
            self.etherpad_id,
            self.summary,
            )
        response = requests.get(url, verify=False, auth=self.etherpad_config['etherpad_auth'])

        if response.status_code == 401:
            raise ImproperlyConfigured("Authentication with pad failed")

        if response.status_code != 200:
            raise ImproperlyConfigured("Problem with pad: {}".format(response))

        response_code = response.json()['code']

        if response_code != 0:
            raise RuntimeError("API request to pad failed: {}".format(response))

    def etherpad_persist(self):
        """Make API call to fetch pad text and write it to the db.

        If the pad doesn't yet exist, it will be created on-the-fly.

        :raises: ImproperlyConfigured   - If there is a problem communicating
                                          with the pad.
        """
        url = "{}/api/1/getText?apikey={}&padID={}".format(
            self.etherpad_config['etherpad_url'],
            self.etherpad_config['etherpad_key'],
            self.etherpad_id,
        )
        response = requests.get(url, verify=False, auth=self.etherpad_config['etherpad_auth'])

        if response.status_code == 401:
            raise ImproperlyConfigured("Authentication with pad failed!")

        if response.status_code != 200:
            raise ImproperlyConfigured("Problem with pad: {}".format(response))

        # Create the pad if it doesn't yet exist.
        response_code = response.json()['code']
        if response_code == 1:
            self.etherpad_create()
            return self.etherpad_persist()

        # Persist pad text to database.
        self.transcript_protocol = response.json()['data']['text']
        self.save()

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

    def save(self, *args, **kwargs):
        super(Topic, self).save(*args, **kwargs)
        if not self.id and self.summary:
            self.etherpad_create()


class TopicRelation(models.Model):
    """Representation of a relation between two topics."""
    class Meta:
        unique_together = ['topic_from', 'topic_to', 'relation']

    # A specific relation always exists between exactly two topics.
    topic_from = models.ForeignKey(Topic, related_name='relation_from')
    topic_to = models.ForeignKey(Topic, related_name='relation_to')

    # A relation is of a specific human-readable type.
    relation = models.IntegerField(choices=TOPIC_RELATIONS, null=True, blank=True)

    def __repr__(self):
        return "{} -> {}".format(self.topic_from.uuid, self.topic_to.uuid)

    def clean(self):
        super(TopicRelation, self).clean()

        if self.topic_from == self.topic_to:
            raise ValidationError("A topic is always related to itself!")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        return super(TopicRelation, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                               update_fields=update_fields)


class Voting(models.Model):
    """Representation of a voting.

    Only circle-members can participate in votings.
    """

    # A voting is always connected to exactly one topic.
    topic = models.OneToOneField(Topic, related_name='voting')

    # There is a formal proposal that in most cases differs slightly
    # from the original topic headline.
    proposal = models.CharField(max_length=1024, db_index=True)

    # There are three different types of votes which are counted and
    # in total should sum up to the total number of attending circle
    # members.
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
    """Representation of a poll.

    All attendees can participate in polls.
    """

    # A poll is always connected to exactly one topic.
    topic = models.OneToOneField(Topic, related_name='polls')

    # It has a formal proposal and outcome.
    proposal = models.CharField(max_length=1024, db_index=True)
    outcome = models.CharField(max_length=8, choices=POLL_OUTCOMES)

    def __str__(self):
        return self.proposal

    @classmethod
    def create(cls, topic, proposal):
        return cls(
            topic=topic,
            proposal=proposal,
        )
