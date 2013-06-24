#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

from wlan_simulation_game.player.models import Player


class Card(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(Player, related_name='cards')
    target = models.ForeignKey(Player, related_name='cards_against_me')
    value = models.IntegerField()
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Karte'
        verbose_name_plural = 'Karten'
        #~ permissions = (
            #~ ("can_play", "Can play a card."),
            #~ ("can_print", "Can see all cards as pdf.")
        #~ )

    def __unicode__(self):
        return self.name

    def play(self):
        """
        Funktion für das Ausspielen einer Karte. Schreibt Punkte gut,
        zieht spielbare Karten ab und verbraucht die Karte. Keine Prüfung der Berechtigung.
        """
        if self.used:
            raise StandardError  # TODO: Raise another error here.
        else:
            self.used = True
            self.save()
            self.owner.playable_cards += -1
            self.owner.save()
            self.target.score += self.value
            self.target.save()
