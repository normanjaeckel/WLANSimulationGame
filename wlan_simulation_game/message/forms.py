#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy

from wlan_simulation_game.player.models import Player

from .models import Message


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
        the view.
        """
        return_value = super(MessageCreateForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].queryset = Player.objects.exclude(pk=request.user.player.pk)
        return return_value


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
