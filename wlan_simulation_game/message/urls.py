#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView

from .models import Message
from .views import MessageListView, MessageCreateView, MessageDetailView, MessagePrintView


urlpatterns = patterns(
    '',
    # List
    url(r'^$',
        login_required(MessageListView.as_view()),
        name='message_list'),
    url(r'^not-printed/$',
        user_passes_test(lambda user: user.is_staff)(ListView.as_view(
            queryset=Message.objects.filter(printed=False).order_by('sending_time'),
            template_name='message/message_list_not_printed.html')),
        name='message_list_not_printed'),
    # Create
    url(r'^create/$',
        login_required(MessageCreateView.as_view()),
        name='message_create'),
    # Detail
    url(r'^(?P<pk>\d+)/$',
        login_required(MessageDetailView.as_view()),
        name='message_detail'),
    # Print
    url(r'^(?P<pk>\d+)/print/$',
        user_passes_test(lambda user: user.is_staff)(MessagePrintView.as_view()),
        name='message_print'))
