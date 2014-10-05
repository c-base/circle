from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100)


class Member(models.Model):
    nick = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group, null=True, blank=True)


class Circle(models.Model):
    circle_id = models.CharField(max_length=10, null=False, unique=True)
    # circle_date = models.DateTimeField('circle_date')
    start = models.DateTimeField('start', null=True, blank=True)
    end = models.DateTimeField('end', null=True, blank=True)
    circle_member_present = models.ManyToManyField(Member, null=True, blank=True, related_name='circle_member_present')
    circle_member_excused = models.ManyToManyField(Member, null=True, blank=True, related_name='circle_member_excused')
    member_present = models.ManyToManyField(Member, null=True, blank=True, related_name='member_present')
    board_present = models.ManyToManyField(Member, null=True, blank=True, related_name='board_present')
    aliens = models.TextField()


class Topic(models.Model):
    circle = models.ForeignKey(Circle)
    subject = models.CharField(max_length=500)
    description = models.TextField()


class Decision(models.Model):
    text = models.CharField(max_length=500)
    topic = models.ForeignKey(Topic)
    pro = models.IntegerField(default=0)
    con = models.IntegerField(default=0)
    abst = models.IntegerField(default=0)


class Opinion(models.Model):
    text = models.CharField(max_length=500)
    topic = models.ForeignKey(Topic)
    result = models.BooleanField(default=True)

