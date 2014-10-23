from django.db import models


class CircleManager(models.Manager):
    def upcoming(self):
        """Return the instance of the upcoming circle session.

        :returns: object    - First instance of upcoming circle sessions.
        """
        for circle in self.get_query_set():
            if circle.upcoming:
                return circle

    def ongoing(self):
        """Return the instance of the ongoing circle session.

        :returns: object    - First instance of ongoing circle sessions.
        """
        for circle in self.get_query_set():
            if circle.ongoing:
                return circle

    def over(self):
        """Return a list of all past circle sessions."""
        return [circle for circle in self.get_query_set() if circle.over]


class TopicManager(models.Manager):
    def upcoming(self, circle=None):
        """Return the list of upcoming topics.

        :param circle:  object  - Limit list to topics of this circle instance.
        :returns: list          - List of upcoming topics.
        """
        if circle is None:
            return [topic for topic in self.get_query_set() if topic.upcoming]
        else:
            return [topic for topic in self.upcoming(circle=None) if topic.circle == circle]

    def ongoing(self):
        """Return the ongoing topic.

        :returns: object    - First instance of ongoing topics.
        """
        for topic in self.get_query_set():
            if topic.ongoing:
                return topic

    def over(self, circle=None):
        """Return a list of all past topics."""
        if circle is None:
            return [topic for topic in self.get_query_set() if topic.over]
        else:
            return [topic for topic in self.over(circle=None) if topic.circle == circle]
