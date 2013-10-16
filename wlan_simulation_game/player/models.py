#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constance import config

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy


class Player(models.Model):
    """
    Model for the player groups. It is one-to-one linked to Django's user
    model but this user model is only used for login.
    """
    user = models.OneToOneField(User, unique=True, verbose_name=ugettext_lazy('Login user'))
    character = models.CharField(max_length=255, unique=True, verbose_name=ugettext_lazy('Character'))
    description = models.TextField(blank=True, verbose_name=ugettext_lazy('Description'))

    class Meta:
        ordering = ('character',)
        verbose_name = ugettext_lazy('Player')
        verbose_name_plural = ugettext_lazy('Players')

    def __unicode__(self):
        return self.character

    @property
    def score(self):
        """
        Returns the actual score of the player according to all played cards.
        """
        value_sum = self.cards_against_me.filter(used=True).aggregate(models.Sum('value'))['value__sum']
        if value_sum is None:
            value_sum = 0
        return config.start_score + value_sum

    @property
    def playable_cards(self):
        """
        Returns the number of playable cards according to the played cards.
        """
        return config.playable_cards - self.cards.filter(used=True).count()

    @property
    def relative_score(self):
        """
        Returns 45/50 of the score. This is just for the bars in the template.
        """
        return self.score * 45 / 50
