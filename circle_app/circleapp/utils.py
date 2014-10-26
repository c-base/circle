class UserMonkeyPatcher(object):
    """Helper properties for patching the builtin django user model."""
    @property
    def is_circle_member(self):
        """Boolean circle membership.

        :returns: bool      - True if user is a circle member.
        """
        return 'circle' in [group.name for group in self.groups.all()]

    @property
    def is_board_member(self):
        """Boolean board membership.

        :returns: bool      - True if user is a board member.
        """
        return 'vorstand' in [group.name for group in self.groups.all()]
