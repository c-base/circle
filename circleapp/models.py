from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100)

class Member(models.Model):
    nick = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group, null=True, blank=True)

class Circle(models.Model):
    circle_date = models.DateTimeField('circle_date')
    start = models.DateTimeField('start')
    end = models.DateTimeField('end')
    circle_member_present = models.ManyToManyField(Member, null=True, blank=True)
    circle_member_excused = models.ManyToManyField(Member, null=True, blank=True)
    member_present = models.ManyToManyField(Member, null=True, blank=True)
    board_present = models.ManyToManyField(Member, null=True, blank=True)

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

