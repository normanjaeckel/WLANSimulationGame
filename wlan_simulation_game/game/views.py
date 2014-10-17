from constance import config
from django.contrib import messages
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import FormView, ListView, DeleteView, DetailView, RedirectView, CreateView

from ..exceptions import WLANSimulationGameError
from .forms import ConventOfferForm, MessageCreateForm, MessageCreateFormStaff
from .models import Card, ConventOffer, Message, Interception


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

    # def get_queryset(self, *args, **kwargs):
        # """
        # Sort cards by owner and target but then shuffle them.
        # """
        # return super().get_queryset(*args, **kwargs).order_by('owner', 'target', '?')


class CardDetailView(DetailView):
    """
    View to see details of a card. Players can only see their own cards in
    detail.
    """
    model = Card

    # def dispatch(self, request, *args, **kwargs):
        # """
        # Method to check that only staff or owners can see their cards.
        # """
        # dispatch = super().dispatch(request, *args, **kwargs)
        # if not request.user.is_staff and not request.user == self.object.owner:
            # messages.error(request, _('You are not owner of this card, so you are not allowed to see it.'))
            # raise PermissionDenied
        # return dispatch


class CardPlayView(RedirectView):
    """
    View to play a bad card.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Method to check if the card is to be played. If yes, it is played.
        After that it redirects to the list of cards.
        """
        card = get_object_or_404(Card, pk=kwargs['pk'])
        if card.is_played():
            messages.error(self.request, _('This card is already played.'))
            raise Http404
        if card.path != 0:
            messages.error(self.request, _('This card can not be played directly.'))
            raise Http404
        if self.request.user != card.bad_playing_player:
            messages.error(self.request, _('This card can only be played by its owner.'))
            raise PermissionDenied
        # TODO: Should a player be able to play more than one bad card? If not, add some logic here.
        card.playing_player = card.bad_playing_player
        card.receiving_player = card.bad_receiving_player
        try:
            card.save()
        except WLANSimulationGameError as error_message:
            messages.error(self.request, error_message)
        else:
            messages.success(self.request, _('Card "%(name)s" was successfully played.') % {'name': card.name})
        return reverse('card_list')


class CardConventView(FormView):
    """
    View to see all offers and to submit a new offer.
    """
    form_class = ConventOfferForm
    success_url = reverse_lazy('card_convent')
    template_name = 'game/convent_form.html'

    def get_context_data(self, **context):
        """
        Adds offers to the context.
        """
        context = super().get_context_data(**context)
        offers = []
        for offer in ConventOffer.objects.filter(
                Q(offeror=self.request.user) | Q (acceptor=self.request.user)):
            if offer.offeror == self.request.user:
                offer_type = 'from_me'
            else:
                offer_type = 'to_me'
            offers.append({'offer': offer, 'type': offer_type})
        context['offers'] = offers
        return context

    def get_form_kwargs(self):
        """
        Hacks in the request for we can use it in the form later.
        """
        form_kwargs = super().get_form_kwargs()
        form_kwargs['request'] = self.request
        return form_kwargs

    def form_valid(self, form):
        """
        Creates an offer.
        """
        ConventOffer.objects.create(
            offeror=self.request.user,
            acceptor=form.cleaned_data['acceptor'],
            offered_card=form.cleaned_data['offered_card'],
            card_in_return=form.cleaned_data['card_in_return'])
        return super().form_valid(form)


class CardConventAcceptView(RedirectView):
    """
    View to accept an offer.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Contains some logic whether the offer is to be accepted.
        """
        offer = get_object_or_404(ConventOffer, pk=kwargs['pk'])

        if not offer.acceptor == self.request.user:
            messages.error(self.request, _('You are not allowed to accept this offer.'))
            raise PermissionDenied

        fail = False
        try:
            with transaction.atomic():
                offered_card = Card.objects.select_for_update().get(pk=offer.offered_card_id)
                if not offered_card.is_played():
                    offered_card.playing_player = offer.offeror
                    offered_card.receiving_player = offer.acceptor
                    if offer.card_in_return_id:
                        card_in_return =  Card.objects.select_for_update().get(pk=offer.card_in_return_id)
                        if not card_in_return.is_played():
                            offered_card.save()
                            offered_card.from_offers.all().delete()
                            offered_card.to_offers.all().delete()
                            card_in_return.playing_player = offer.acceptor
                            card_in_return.receiving_player = offer.offeror
                            card_in_return.save()
                            card_in_return.from_offers.all().delete()
                            card_in_return.to_offers.all().delete()
                        else:
                            messages.error(self.request, _('The offer can not be accepted any more because the card in return was already played.'))
                            fail=True
                    else:
                        offered_card.save()
                        offered_card.from_offers.all().delete()
                        offered_card.to_offers.all().delete()
                else:
                    messages.error(self.request, _('The offer can not be accepted any more because the offered card was already played.'))
                    fail = True
        except IntegrityError:
            messages.error(self.request, 'Unknown IntegrityError')
        except WLANSimulationGameError as error_message:
            messages.error(self.request, error_message)
        else:
            if not fail:
                messages.success(self.request, _('Offer successfully accepted. Look at your new score if you like.'))

        return reverse('card_convent')


class CardConventDeleteView(RedirectView):
    """
    View to delete offers. Either the offeror or the acceptor can delete an
    offer.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Method to check if the user is allowed to delete the convent offer.
        If yes, the offer will be deleted and the user is redirected to the
        convent page. If no, a 403 is raised.
        """
        offer = get_object_or_404(ConventOffer, pk=kwargs['pk'])
        if not offer.offeror == self.request.user and not offer.acceptor == self.request.user:
            messages.error(self.request, _('You are not allowed to delete this offer.'))
            raise PermissionDenied
        offer.delete()
        messages.success(self.request, _('Offer successfully deleted.'))
        return reverse('card_convent')


# class CardPlayView(RedirectView):
    # """
    # View to play a card.

    # A card is played, when it exists, is not already used and the owner can
    # still play at least one card. In urls.py it is checked that the
    # request.user is staff.
    # """
    # permanent = False

    # def get_redirect_url(self, *args, **kwargs):
        # """
        # Method to check if the card is to be played. If yes, it is played.
        # After that it redirects to the list of cards.
        # """
        # card = get_object_or_404(Card, pk=kwargs['pk'])
        # try:
            # card.play()
        # except WLANSimulationGameError as error_message:
            # messages.error(self.request, error_message)
        # else:
            # messages.success(self.request, _('Card "%(name)s" was successfully played.') % {'name': card.name})
        # return reverse('card_list')
