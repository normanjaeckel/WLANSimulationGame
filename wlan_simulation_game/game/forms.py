import datetime

from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.utils.timezone import localtime, now

from .models import Card, ConventOffer, Message, Player


class MessageCreateForm(forms.ModelForm):
    """
    Form for new messages for non staff users.
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
        Manipulate recipient field to exclude the request user player and
        staff users. The request object is excluded from the kwargs for it
        was hacked in in the view. It is attached to the form for later use.
        """
        self.request = request
        return_value = super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = Player.objects.filter(is_staff=False).exclude(pk=self.request.user.pk)
        return return_value

    def clean(self, *args, **kwargs):
        """
        Checks the time limit for messages to the same recipient.
        """
        minutes_to_wait = 3
        cleaned_data = super().clean(*args, **kwargs)
        time_limit = localtime(now()) - datetime.timedelta(minutes=minutes_to_wait)
        if cleaned_data.get('recipient') and Message.objects.filter(
                sender=self.request.user,
                recipient=cleaned_data['recipient'],
                sending_time__gt=time_limit.time()).exists():
            raise forms.ValidationError(
                _('You have to wait %d minutes before you can send the next message to the same recipient.') % minutes_to_wait)
        return cleaned_data


class MessageCreateFormStaff(forms.ModelForm):
    """
    Form for new messages for staff users.
    """
    sender = forms.ModelChoiceField(
        empty_label=None,
        label=ugettext_lazy('Sender'),
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
        return super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        """
        Checks that the sender is not the recipient.
        """
        cleaned_data = super().clean(*args, **kwargs)
        if (cleaned_data.get('sender') and cleaned_data.get('recipient') and
                cleaned_data['sender'] == cleaned_data['recipient']):
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
        Manipulate victim_sender field to exclude the request user player
        and staff users. The request object is excluded from the kwargs for
        it was hacked in in the view.
        """
        return_value = super().__init__(*args, **kwargs)
        self.fields['victim_sender'].queryset = Player.objects.filter(is_staff=False).exclude(pk=request.user.pk)
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
        Manipulate victim_recipient field to exclude the request user
        player, staff users and the victim_sender. The request object and
        the victim_sender are excluded from the kwargs for they were hacked
        in in the view.
        """
        return_value = super().__init__(*args, **kwargs)
        self.fields['victim_recipient'].queryset = Player.objects.filter(is_staff=False).exclude(pk=request.user.pk).exclude(pk=victim_sender.pk)
        return return_value


class ConventOfferForm(forms.Form):
    """
    Form to submit a new offer.
    """
    acceptor = forms.ModelChoiceField(
        empty_label=None,
        label=ugettext_lazy('Acceptor'),
        queryset=Player.objects.all())
    offered_card = forms.ModelChoiceField(
        empty_label=None,
        label=ugettext_lazy('Offered Card'),
        queryset=Card.objects.exclude(path=0))
    acceptor = forms.ModelChoiceField(
        label=ugettext_lazy('Card in return'),
        required=False,
        queryset=Card.objects.all())

    def __init__(self, *arg, **kwargs):
        """
        """

