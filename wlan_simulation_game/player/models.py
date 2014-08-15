from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy


class PlayerManager(UserManager):
    """
    Custom manager to disable email as required field for superusers.
    """
    def create_superuser(self, *args, **kwargs):
        kwargs.setdefault('email')
        return super().create_superuser(*args, **kwargs)


class Player(AbstractUser):
    """
    Model for the player groups.
    """
    description = models.TextField(blank=True, verbose_name=ugettext_lazy('Description'))

    objects = PlayerManager()

    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('is_staff', 'username',)
        verbose_name = ugettext_lazy('Player')
        verbose_name_plural = ugettext_lazy('Players')

    @property
    def score(self):
        """
        Returns the actual score of the player according to all played cards.
        """
        from constance import config
        value_sum = self.cards_against_me.filter(used=True).aggregate(models.Sum('value'))['value__sum']
        if value_sum is None:
            value_sum = 0
        return config.start_score + value_sum

    @property
    def playable_cards(self):
        """
        Returns the number of playable cards according to the played cards.
        """
        from constance import config
        return config.playable_cards - self.cards.filter(used=True).count()

    @property
    def relative_score(self):
        """
        Returns 45/50 of the score. This is just for the bars in the template.
        """
        return self.score * 45 / 50
