#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django import forms
from django.utils.translation import ugettext as _, ugettext_lazy
from django.utils.timezone import localtime, now

from wlan_simulation_game.player.models import Player

from .models import Message, Interception


class MessageCreateForm(forms.ModelForm):
    """
    Form for new messages for players.
    """
    recipient = forms.ModelChoiceField(
        empty_label=None,
        label=ugettext_lazy('Recipient'),
        queryset=Player.objects.all())

    class Meta:
        model = Message
        exclude = ('printed', 'sender')

    def __init__(self, request, *args, **kwargs):
        """
        Manipulate recipient field to exclude the request user player. The
        request object is excluded from the kwargs for it was hacked in in
        the view. It is attached to the form for later use.
        """
        self.request = request
        return_value = super(MessageCreateForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].queryset = Player.objects.exclude(pk=self.request.user.player.pk)
        return return_value

    def clean(self, *args, **kwargs):
        """
        Checks the time limit for messages to the same recipient.
        """
        cleaned_data = super(MessageCreateForm, self).clean(*args, **kwargs)
        minutes_to_wait = 3
        time_limit = localtime(now()) - datetime.timedelta(minutes=minutes_to_wait)
        if Message.objects.filter(
                sender=self.request.user.player,
                recipient=cleaned_data['recipient'],
                sending_time__gt=time_limit.time()).exists():
            raise forms.ValidationError(
                _('You have to wait %d minutes before you can send the next message to the same recipient.') % minutes_to_wait)
        return cleaned_data


class MessageCreateFormStaff(forms.ModelForm):
    """
    Form for new messages for staff.
    """
    sender = forms.ModelChoiceField(
        empty_label=ugettext_lazy('Game Master'),
        label=ugettext_lazy('Sender'),
        required=False,
        queryset=Player.objects.all())
    recipient = forms.ModelChoiceField(
        empty_label=ugettext_lazy('All players'),
        label=ugettext_lazy('Recipient'),
        required=False,
        queryset=Player.objects.all())

    class Meta:
        model = Message
        exclude = ('printed',)

    def __init__(self, request, *args, **kwargs):
        """
        The request object is excluded from the kwargs for it was hacked in
        in the view.
        """
        return super(MessageCreateFormStaff, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        """
        Checks that the sender is not the recipient.
        """
        cleaned_data = super(MessageCreateFormStaff, self).clean(*args, **kwargs)
        if cleaned_data['sender'] and cleaned_data['recipient'] == cleaned_data['sender']:
            raise forms.ValidationError(_('You can not send a message from a player to himself.'))
        return cleaned_data


class InterceptionWizardFormOne(forms.Form):
    """
    Form one for a new interception.
    """
    victim_sender = forms.ModelChoiceField(
        label=ugettext_lazy('Victim Sender'),
        queryset=Player.objects.all())

    def __init__(self, request, *args, **kwargs):
        """
        Manipulate victim_sender field to exclude the request user player. The
        request object is excluded from the kwargs for it was hacked in in
        the view.
        """
        return_value = super(InterceptionWizardFormOne, self).__init__(*args, **kwargs)
        self.fields['victim_sender'].queryset = Player.objects.exclude(pk=request.user.player.pk)
        return return_value


class InterceptionWizardFormTwo(forms.Form):
    """
    Form two for a new interception.
    """
    victim_recipient = forms.ModelChoiceField(
        label=ugettext_lazy('Victim Recipient'),
        queryset=Player.objects.all())

    def __init__(self, request, victim_sender=None, *args, **kwargs):
        """
        Manipulate victim_recipient field to exclude the request user player
        and the victim_sender. The request object and the victim_sender are
        excluded from the kwargs for they were hacked in in the view.
        """
        return_value = super(InterceptionWizardFormTwo, self).__init__(*args, **kwargs)
        self.fields['victim_recipient'].queryset = Player.objects.exclude(pk=request.user.player.pk).exclude(pk=victim_sender.pk)
        return return_value
