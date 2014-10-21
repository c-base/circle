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
