#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, RedirectView

from wlan_simulation_game.exceptions import WLANSimulationGameError

from .models import Card


class CardListView(ListView):
    """
    View to see all cards.
    """
    model = Card

    def get_queryset(self, *args, **kwargs):
        """
        Sort cards by owner and target but then shuffle them.
        """
        return super(CardListView, self).get_queryset(*args, **kwargs).order_by('owner', 'target', '?')


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
        dispatch = super(CardDetailView, self).dispatch(request, *args, **kwargs)
        if not request.user.is_staff and not request.user.player == self.object.owner:
            messages.error(request, _('You are not owner of this card, so you are not allowed to see it.'))
            raise PermissionDenied
        return dispatch


class CardPlayView(RedirectView):
    """
    View to play a card.

    A card is played, when it exists, is not already used, the owner can still
    play at least one card and the request.user is staff.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Method to check if the card is to be played. If yes, it is played.
        After that it redirects to the list of cards.
        """
        if not self.request.user.is_staff:
            messages.error(self.request, _('You are not allowed to play a card via this interface.'))
            raise PermissionDenied
        card = get_object_or_404(Card, pk=kwargs['pk'])
        try:
            card.play()
        except WLANSimulationGameError, error_message:
            messages.error(self.request, error_message)
        else:
            messages.success(self.request, _('Card "%(name)s" was successfully played.') % {'name': card.name})
        return reverse('card_list')
