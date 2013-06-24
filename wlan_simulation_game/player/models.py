#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy

class Player(models.Model):
    """
    Model for the five player groups. It is one-to-one linked to Django's user
    model but this user model is only used for login.
    """
    user = models.OneToOneField(User, unique=True, verbose_name=ugettext_lazy('Login user'))
    character = models.CharField(max_length=255, unique=True, verbose_name=ugettext_lazy('Character'))
    description = models.TextField(verbose_name=ugettext_lazy('Description'))
    score = models.IntegerField(default=20, verbose_name=ugettext_lazy('Score'))
    playable_cards = models.IntegerField(default=5, verbose_name=ugettext_lazy('Playable Cards'))

    class Meta:
        verbose_name = ugettext_lazy('Player')
        verbose_name_plural = ugettext_lazy('Players')

    def __unicode__(self):
        return self.character

    @property
    def relative_score(self):
        return self.score * 45 / 50
