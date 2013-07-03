#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, RedirectView, CreateView

from .forms import MessageCreateForm, MessageCreateFormStaff
from .models import Message


class MessageListView(ListView):
    """
    View to see all own messages
    """
    model = Message

    def get_queryset(self, *args, **kwargs):
        """
        Players can only see their own messages.
        """
        queryset = super(MessageListView, self).get_queryset(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset = queryset.filter(sender=self.request.user.player)
        return queryset


class MessageDetailView(DetailView):
    """
    View to see a single message.
    """
    model = Message

    def dispatch(self, request, *args, **kwargs):
        """
        Method to check that only staff or senders can see their messages.
        """
        dispatch = super(MessageDetailView, self).dispatch(request, *args, **kwargs)
        if request.user.is_staff or request.user.player == self.object.sender:
            return dispatch
        else:
            messages.error(request, _('You are not allowed to see this message.'))
            raise PermissionDenied


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

    def get_form_class(self, *args, **kwargs):
        """
        Returns one of the two create forms, either for normal users or for
        staff.
        """
        if self.request.user.is_staff:
            return MessageCreateFormStaff
        else:
            return MessageCreateForm

    def get_form_kwargs(self, *args, **kwargs):
        """
        Hacks in the request for we can use it in the form later.
        """
        kwargs = super(MessageCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """
        Adds missing sender, if a player (non staff) sends a message, and saves
        the object.
        """
        if self.request.user.is_staff:
            return super(MessageCreateView, self).form_valid(form)
        else:
            self.object = form.save(commit=False)
            self.object.sender = self.request.user.player
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
