from django.db import models


class CircleManager(models.Manager):
    def upcoming(self):
        for circle in self.get_query_set():
            if circle.upcoming:
                return circle

    def ongoing(self):
        for circle in self.get_query_set():
            if circle.ongoing:
                return circle

    def over(self):
        return [circle for circle in self.get_query_set() if circle.over]


class TopicManager(models.Manager):
    def upcoming(self):
        for topic in self.get_query_set():
            if topic.upcoming:
                return topic

    def ongoing(self):
        for topic in self.get_query_set():
            if topic.ongoing:
                return topic

    def over(self):
        return [topic for topic in self.get_query_set() if topic.over]
