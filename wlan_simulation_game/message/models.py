#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy

from wlan_simulation_game.exceptions import WLANSimulationGameError
from wlan_simulation_game.player.models import Player


class Message(models.Model):
    """
    Model for messages between players and messages from the admin to all
    players.
    """
    sender = models.ForeignKey(
        Player,
        null=True,
        blank=True,
        related_name='sent_messages',
        verbose_name=ugettext_lazy('Sender'))
    recipient = models.ForeignKey(
        Player,
        null=True,
        blank=True,
        related_name='received_messages',
        verbose_name=ugettext_lazy('Recipient'))
    subject = models.CharField(max_length=32, verbose_name=ugettext_lazy('Subject'))
    text = models.TextField(verbose_name=ugettext_lazy('Text'))
    printed = models.BooleanField(default=False, verbose_name=ugettext_lazy('Printed'))
    sending_time = models.TimeField(auto_now_add=True, verbose_name=ugettext_lazy('Sending Time'))

    class Meta:
        verbose_name = ugettext_lazy('Message')
        verbose_name_plural = ugettext_lazy('Messages')

    def save(self, *args, **kwargs):
        """
        Override to check that no one is sender and recipient at one time.
        """
        if self.sender == self.recipient:
            raise WLANSimulationGameError, _('The sender can not be saved as recipient.')
        return super(Message, self).save(*args, **kwargs)

    def __unicode__(self):
        """
        Method for representation.
        """
        return _('Message %(number)d: %(subject)s') % {'number': self.pk, 'subject': self.subject}

    #~ def wurde_gedruckt(self):
        #~ self.gedruckt = True
        #~ self.save()
