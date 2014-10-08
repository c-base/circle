from django.db import models
from django.core.exceptions import ValidationError
from circle.models import Member, Alien
from hashlib import md5

ETHERPAD_BASE_URL = "https://pad.c-base.org/p/circle"


class Circle(models.Model):
    class Meta:
        ordering = ['date']

    # A circle takes place an a regular date and there is only one meeting on
    # that date.
    date = models.DateField(unique=True, db_index=True)

    # A circle is formally opened and closed by timestamp.
    opened = models.DateTimeField(null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)

    # There are several different kinds of attendees to a circle.
    attending_circle_members = models.ManyToManyField(Member, null=True, blank=True,
                                                      related_name='circles_where_circle_member')
    attending_board_members = models.ManyToManyField(Member, null=True, blank=True,
                                                     related_name='circles_where_board_member')
    attending_regular_members = models.ManyToManyField(Member, null=True, blank=True,
                                                       related_name='circles_where_regular_member')
    attending_aliens = models.ManyToManyField(Alien, null=True, blank=True,
                                              related_name='circles_where_alien')

    # Every circle has a designated moderator...
    moderator = models.ForeignKey(Member, related_name='moderated_circles')

    # ... and 1-n transcript writers.
    transcript_writers = models.ManyToManyField(Member, related_name='transcript_circles')

    def __str__(self):
        return "Circle-{}".format(self.date.strftime("%Y-%m-%d"))

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

    def clean_field_date(self):
        """Validate changes to the date attribute."""
        old_instance = Circle.objects.get(pk=self.pk)
        print self.date, old_instance.date
        if self.date != old_instance.date:
            raise ValidationError("Changing the date is not allowed!")

    def clean_field_opened(self):
        """Validate changes to the opened attribute."""
        old_instance = Circle.objects.get(pk=self.pk)
        if self.opened != old_instance.opened:

            if not self.opened:
                raise ValidationError("Opening a circle is irreversible!")

            if len(self.attending_circle_members.all()) < 5:
                raise ValidationError("At least five circle-members must be attending!")

            if not self.moderator:
                raise ValidationError("Can not opened circle before a moderator has been declared!")

            if len(self.transcript_writers.all()) < 1:
                raise ValidationError("Can not open circle before at least one transcript writer has been declared!")

            # Todo: When at least one topic is present.

    def clean_field_closed(self):
        """Validate changes to the closed attribute."""
        old_instance = Circle.objects.get(pk=self.pk)
        if self.closed != old_instance.closed:

            if not self.closed:
                raise ValidationError("Closing a circle is irreversible!")

            if not self.opened:
                raise ValidationError("Can not close circle before opening it!")

            # Todo: When all topics are closed.

    def clean_field_attending_circle_members(self):
        """Validate changes on the attendee attributes."""
        old_instance = Circle.objects.get(pk=self.pk)
        if self.attending_circle_members != old_instance.attending_circle_members:

            if self.closed:
                raise ValidationError("Can not change attendees after circle has been closed!")

            if self.ongoing and len(self.attending_circle_members.all()) < 5:
                raise ValidationError("At least five circle-members must be attending!")

            if self.closed:
                raise ValidationError("Can not change attendees after circle has been closed!")

    def clean_field_moderator(self):
        """Validate changes to the moderator attribute."""
        old_instance = Circle.objects.get(pk=self.pk)
        if self.moderator != old_instance.moderator:

            if not self.upcoming:
                raise ValidationError("Moderators can only be declared before the circle is formally opened!")

    def clean_field_transcript_writer(self):
        """Validate changes to the transcript_writer attribute."""
        old_instance = Circle.objects.get(pk=self.pk)
        if self.transcript_writers.all() != old_instance.transcript_writers.all():

            if self.ongoing:

                if len(self.transcript_writers.all()) == 0:
                    raise ValidationError("At least one transcript writer must be declared ongoing during circle!")

            if self.locked:
                raise ValidationError("Can not change transcripters after circle has been closed!")

    def clean_fields(self, exclude=None):
        super(Circle, self).clean_fields(exclude=exclude)

        if self.pk:
            self.clean_field_date()
            self.clean_field_opened()
            self.clean_field_closed()
            self.clean_field_attendees()
            self.clean_field_moderator()
            self.clean_field_transcript_writer()

    def save(self, *args, **kwargs):
        self.clean_fields()
        return super(Circle, self).save(*args, **kwargs)

    def delete(self, using=None, force=False):
        if force is True:
            return super(Circle, self).delete(using=using)


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

    def clean_circle(self):
        """Validate changes to the circle attribute."""
        old_instance = Topic.objects.get(pk=self.pk)

        if self.circle != old_instance.circle:
            raise ValidationError("Changing circle of a topic is illegal!")

    def clean_order(self):
        """Validate changes to the order attribute."""
        old_instance = Topic.objects.get(pk=self.pk)

        if self.order != old_instance.order:
            if self.circle.locked:
                raise ValidationError("Can not change order after circle has been closed!")

    def clean_headline(self):
        """Validate changes to the headline attribute."""
        old_instance = Topic.objects.get(pk=self.pk)

        if self.headline != old_instance.headline:

            if self.ongoing:
                raise ValidationError("Can not change headline after topic has been opened!")

            if self.locked:
                raise ValidationError("Can not change headline after topic has been closed!")

    def clean_etherpad(self):
        """Generate and set the etherpad link."""
        self.etherpad = self.etherpad_link

    def clean_opened(self):
        """Validate changes to the opened attribute."""
        old_instance = Topic.objects.get(pk=self.pk)

        if self.opened != old_instance.opened:

            if not self.opened:
                raise ValidationError("Can not closed already opened topics!")

            if self.locked:
                raise ValidationError("Can not open topics that are already closed!")

    def clean_closed(self):
        """Validate changes to the closed attribute."""
        old_instance = Topic.objects.get(pk=self.pk)

        if self.closed != old_instance.closed:

            if not self.closed:
                raise ValidationError("Closing a topic is irreversible!")

            if not self.opened:
                raise ValidationError("Can not close a topic before opening it!")

    def clean(self):
        super(Topic, self).clean()

        if self.pk:
            self.clean_circle()
            self.clean_order()
            self.clean_headline()
            self.clean_etherpad()
            self.clean_opened()
            self.clean_closed()
        else:
            if not self.circle.ongoing:
                raise ValidationError("Can not create topics in circles that aren't currently ongoing!")

    def save(self, *args, **kwargs):
        self.clean()
        return super(Topic, self).save(*args, **kwargs)

    def delete(self, using=None, force=False):
        if force is True:
            return super(Topic, self).delete(using=using)


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

    def clean(self):
        super(Voting, self).clean()

        if self.topic.locked:
            raise ValidationError("Can not change voting on closed topic!")

    def save(self, *args, **kwargs):
        self.clean()
        return super(Voting, self).save(*args, **kwargs)

    def delete(self, using=None, force=False):
        if force is True:
            return super(Voting, self).delete(using=using)


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

    def clean(self):
        super(Poll, self).clean()

        if not self.pk:
            if not self.topic.ongoing:
                raise ValidationError("Can not create poll if topic is not currently open!")

    def save(self, *args, **kwargs):
        self.clean()
        return super(Poll, self).save(*args, **kwargs)

    def delete(self, using=None, force=False):
        if force is True:
            return super(Poll, self).delete(using=using)
