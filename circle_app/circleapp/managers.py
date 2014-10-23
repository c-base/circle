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
    def upcoming(self, circle=None):
        """Return the list of upcoming topics.

        :param circle:  object  - Limit list to topics of this circle instance.
        """
        if circle is None:
            return [topic for topic in self.get_query_set() if topic.upcoming]
        else:
            return [topic for topic in self.upcoming(circle=None) if topic.circle == circle]

    def ongoing(self):
        for topic in self.get_query_set():
            if topic.ongoing:
                return topic

    def over(self, circle=None):
        if circle is None:
            return [topic for topic in self.get_query_set() if topic.over]
        else:
            return [topic for topic in self.over(circle=None) if topic.circle == circle]
