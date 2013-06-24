#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, unique=True)
    character = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    score = models.IntegerField(default=20)
    playable_cards = models.IntegerField(default=5)

    class Meta:
        verbose_name = 'Spieler'
        verbose_name_plural = 'Spieler'

    def __unicode__(self):
        return self.character

    @property
    def relative_score(self):
        return self.score * 45 / 50
