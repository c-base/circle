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

    def current(self):
        ongoing = self.ongoing()
        if ongoing:
            return ongoing

        upcoming = self.upcoming()
        if upcoming:
            return upcoming


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

    def formal_order(self, circle):
        """Alien topics go before member topics."""
        return [
            topic for topic in self.get_query_set()
            if topic.circle == circle
            and topic.applicant_alien
        ] + [
            topic for topic in self.get_query_set()
            if topic.circle == circle
            and topic.applicant_member
        ]


class ParticipantManager(models.Manager):
    def _get_current_circle(self):
        from circleapp.models import Circle
        return Circle.objects.current()

    def list(self, circle=None):
        """Return all participants of a circle session.

        :returns: list      - List of Member() instances.
        """
        circle = circle or self._get_current_circle()
        return [participation.user for participation in self.get_query_set() if participation.circle == circle]

    def circle_members(self, circle=None):
        """Return all participating circle-members of a circle session.

        :returns: list      - List of Member() instances.
        """
        circle = circle or self._get_current_circle()
        return [
            participation.user for participation in self.get_query_set()
            if participation.circle == circle
            and participation.user.is_circle_member
        ]

    def board_members(self, circle=None):
        """Return all board-members of a circle session.

        :returns: list      - List of Member() instances.
        """
        circle = circle or self._get_current_circle()
        return [
            participation.user for participation in self.get_query_set()
            if participation.circle == circle
            and participation.user.is_board_member
        ]

    def transcript_writers(self, circle=None):
        """Return all transcript writers of a circle session.

        :returns: list      - List of Member() instances.
        """
        circle = circle or self._get_current_circle()
        return [
            participation.user for participation in self.get_query_set()
            if participation.circle == circle
            and participation.role == 'writer'
        ]

    def moderator(self, circle=None):
        """Return moderator of a circle session.

        :returns: object    - Instance of Member()
        """
        circle = circle or self._get_current_circle()
        for participation in self.get_query_set():
            if participation.circle == circle:
                if participation.role == 'mod':
                    return participation
