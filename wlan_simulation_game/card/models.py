#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy

from wlan_simulation_game.exceptions import WLANSimulationGameError
from wlan_simulation_game.player.models import Player


class Card(models.Model):
    """
    Model for a card that one player, the owner, can play with respect to
    another player, the target.
    """
    name = models.CharField(max_length=255, verbose_name=ugettext_lazy('Name'))
    description = models.TextField(blank=True, verbose_name=ugettext_lazy('Description'))
    owner = models.ForeignKey(Player, related_name='cards', verbose_name=ugettext_lazy('Owner'))
    target = models.ForeignKey(Player, related_name='cards_against_me', verbose_name=ugettext_lazy('Target'))
    value = models.IntegerField(verbose_name=ugettext_lazy('Value'))
    used = models.BooleanField(default=False, verbose_name=ugettext_lazy('Used'))

    class Meta:
        verbose_name = ugettext_lazy('Card')
        verbose_name_plural = ugettext_lazy('Cards')

    def save(self, *args, **kwargs):
        """
        Override to check that no one is owner and target at one time.
        """
        if self.owner == self.target:
            raise WLANSimulationGameError, _('The owner can not be saved as target.')
        return super(Card, self).save(*args, **kwargs)

    def __unicode__(self):
        """
        Method for representation.
        """
        return self.name

    def play(self):
        """
        Method to play a card. No check of permissions.
        """
        if self.used:
            raise WLANSimulationGameError, _('You can not play this card any more. It is already used.')
        elif self.owner.playable_cards <= 0:
            raise WLANSimulationGameError, _('The owner can not play cards anymore.')
        else:
            self.used = True
            self.save()
            self.owner.playable_cards += -1
            self.owner.save()
            self.target.score += self.value
            self.target.save()
