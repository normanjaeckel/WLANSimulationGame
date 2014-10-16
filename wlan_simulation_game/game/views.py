from constance import config
from django.contrib import messages
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, RedirectView, CreateView

from ..exceptions import WLANSimulationGameError
from .forms import MessageCreateForm, MessageCreateFormStaff
from .models import Card, Message, Interception


class MessageListView(ListView):
    """
    View to see all own messages.
    """
    model = Message

    def get_queryset(self, *args, **kwargs):
        """
        Players can only see their own messages or intercepted messages.
        """
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(sender=self.request.user) | Q(interception__interceptor=self.request.user))
        return queryset


class MessageDetailView(DetailView):
    """
    View to see a single message.
    """
    model = Message

    def dispatch(self, request, *args, **kwargs):
        """
        Method to check that only staff or senders can see their messages
        (or intercepted messages).
        """
        dispatch = super().dispatch(request, *args, **kwargs)
        if (not request.user.is_staff and
                not request.user == self.object.sender and
                not self.object.interception_set.filter(interceptor=request.user).exists()):
            messages.error(request, _('You are not allowed to see this message.'))
            raise PermissionDenied
        else:
            # Everything is ok, the message can be shown.
            pass
        return dispatch


class MessagePrintView(RedirectView):
    """
    View to mark a message as printed.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Method to check if the message is already printed. If no, it is marked
        as printed. After that it redirects to the list of not printed
        messages.
        """
        message = get_object_or_404(Message, pk=kwargs['pk'])
        if not message.printed:
            message.printed = True
            message.save()
        else:
            messages.error(self.request, _('The message was already marked as printed.'))
        return reverse('message_list_not_printed')


class MessageCreateView(CreateView):
    """
    View to write a new message.
    """
    model = Message

    def dispatch(self, request, *args, **kwargs):
        """
        Checks the config variable 'players_can_submit_messages'.
        """
        if not request.user.is_staff and not config.players_can_submit_messages:
            messages.error(request, _('You are not allowed to send a message at the moment.'))
            raise PermissionDenied
        else:
            # Everything is ok, the message can be created.
            pass
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self, *args, **kwargs):
        """
        Returns one of the two create forms, either for normal users or for
        staff.
        """
        if self.request.user.is_staff:
            form = MessageCreateFormStaff
        else:
            form = MessageCreateForm
        return form

    def get_form_kwargs(self, *args, **kwargs):
        """
        Hacks in the request for we can use it in the form later.
        """
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['request'] = self.request
        return form_kwargs

    def form_valid(self, form):
        """
        Adds missing sender if a player (non staff) sends a message, and saves
        the object.
        """
        if self.request.user.is_staff:
            return_value = super().form_valid(form)
        else:
            self.object = form.save(commit=False)
            self.object.sender = self.request.user
            self.object.save()
            return_value = HttpResponseRedirect(self.get_success_url())
        return return_value


class InterceptionWizardView(SessionWizardView):
    """
    View to intercept messages.
    """
    template_name = 'game/interception_wizard_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Checks whether the user as already intercepted enough messages.
        """
        if request.user.is_staff:
            messages.error(request, _('The interception view is only for players.'))
            raise PermissionDenied
        elif Interception.objects.filter(interceptor=request.user).count() >= config.number_of_interceptions:
            messages.error(request, _('You can only intercept a total number of %d messages.') % config.number_of_interceptions)
            raise PermissionDenied
        else:
            # Everything is ok, intercept now.
            pass
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, step):
        """
        Hacks in the request for we can use it in the form later.
        """
        form_kwargs = super().get_form_kwargs(step)
        form_kwargs['request'] = self.request
        if step == '1':
            form_kwargs['victim_sender'] = self.get_cleaned_data_for_step('0')['victim_sender']
        return form_kwargs

    def done(self, form_list, **kwargs):
        """
        Processes the valid form data.
        """
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        message_list = Message.objects.filter(sender=data['victim_sender'], recipient=data['victim_recipient']).reverse()
        if not message_list:
            messages.error(self.request, _('There is no message to intercept between these two players. Try again later.'))
        else:
            try:
                Interception.objects.create(interceptor=self.request.user, message=message_list[0])
            except WLANSimulationGameError as error:
                messages.error(self.request, error.args[0])
            else:
                messages.success(self.request, _('The message was succesfully intercepted. You can read it now.'))
        return HttpResponseRedirect(reverse('message_list'))


class CardListView(ListView):
    """
    View to see all cards.
    """
    model = Card

    def get_queryset(self, *args, **kwargs):
        """
        Sort cards by owner and target but then shuffle them.
        """
        return super().get_queryset(*args, **kwargs).order_by('owner', 'target', '?')


class CardDetailView(DetailView):
    """
    View to see details of a card. Players can only see their own cards in
    detail.
    """
    model = Card

    def dispatch(self, request, *args, **kwargs):
        """
        Method to check that only staff or owners can see their cards.
        """
        dispatch = super().dispatch(request, *args, **kwargs)
        if not request.user.is_staff and not request.user == self.object.owner:
            messages.error(request, _('You are not owner of this card, so you are not allowed to see it.'))
            raise PermissionDenied
        return dispatch


class CardPlayView(RedirectView):
    """
    View to play a card.

    A card is played, when it exists, is not already used and the owner can
    still play at least one card. In urls.py it is checked that the
    request.user is staff.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Method to check if the card is to be played. If yes, it is played.
        After that it redirects to the list of cards.
        """
        card = get_object_or_404(Card, pk=kwargs['pk'])
        try:
            card.play()
        except WLANSimulationGameError as error_message:
            messages.error(self.request, error_message)
        else:
            messages.success(self.request, _('Card "%(name)s" was successfully played.') % {'name': card.name})
        return reverse('card_list')
