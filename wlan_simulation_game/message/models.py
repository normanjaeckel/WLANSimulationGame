#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constance import config

from django.db import models, IntegrityError
from django.utils.translation import ugettext as _, ugettext_lazy

from wlan_simulation_game.exceptions import WLANSimulationGameError
from wlan_simulation_game.player.models import Player


class Message(models.Model):
    """
    Model for messages between players.

    If the sender is None, it means that the sender is the game master. If the
    recepient is None, it means that it is a message to all players.
    """
    sender = models.ForeignKey(
        Player,
        null=True,
        related_name='sent_messages',
        verbose_name=ugettext_lazy('Sender'))
    recipient = models.ForeignKey(
        Player,
        null=True,
        related_name='received_messages',
        verbose_name=ugettext_lazy('Recipient'))
    subject = models.CharField(max_length=32, verbose_name=ugettext_lazy('Subject'))
    text = models.TextField(verbose_name=ugettext_lazy('Text'))
    printed = models.BooleanField(default=False, verbose_name=ugettext_lazy('Printed'))
    sending_time = models.TimeField(auto_now_add=True, verbose_name=ugettext_lazy('Sending Time'))

    class Meta:
        ordering = ('sender', 'recipient', 'sending_time')
        verbose_name = ugettext_lazy('Message')
        verbose_name_plural = ugettext_lazy('Messages')

    def save(self, *args, **kwargs):
        """
        Override to check that no one is sender and recipient at one time.
        """
        if self.sender == self.recipient and self.sender is not None:
            raise WLANSimulationGameError(_('The sender can not be saved as recipient.'))
        return super(Message, self).save(*args, **kwargs)

    def __unicode__(self):
        """
        Method for representation.
        """
        return self.subject

    @models.permalink
    def get_absolute_url(self):
        """
        Url to the detail view.
        """
        return ('message_detail', [str(self.pk)])


class Interception(models.Model):
    """
    Model for an interception by one player against two others.
    """
    interceptor = models.ForeignKey(
        Player,
        verbose_name=ugettext_lazy('Interceptor'))
    message = models.ForeignKey(
        Message,
        verbose_name=ugettext_lazy('Message'))

    class Meta:
        unique_together = ('interceptor', 'message')
        verbose_name = ugettext_lazy('Interception')
        verbose_name_plural = ugettext_lazy('Interceptions')

    def save(self, *args, **kwargs):
        """
        Override to check that a player can only intercept messages of other
        players and only the allowed number of messages.
        """
        if self.message.sender is None:
            raise WLANSimulationGameError(_('You can not intercept messages from the game master.'))
        if (self.message.sender == self.interceptor or
                self.message.recipient == self.interceptor or
                self.message.recipient is None):
            raise WLANSimulationGameError(_('You can not intercept a message from or to yourself.'))
        if Interception.objects.filter(interceptor=self.interceptor).count() >= config.number_of_interceptions:
            raise WLANSimulationGameError(_('You can only intercept a total number of %d messages') % config.number_of_interceptions)
        try:
            return_value = super(Interception, self).save(*args, **kwargs)
        except IntegrityError as error:
            if error.args[0] == 'columns interceptor_id, message_id are not unique':
                error_message = _('There is no new message you have not intercepted yet. Try again later.')
            else:
                error_message = error.args
            raise WLANSimulationGameError(error_message)
        return return_value

    def __unicode__(self):
        """
        Method for representation.
        """
        return '%s -- %s (%s an %s)' % (self.interceptor, self.message, self.message.sender, self.message.recipient)
