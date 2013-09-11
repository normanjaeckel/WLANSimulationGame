#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, user_passes_test

from .views import CardListView, CardDetailView, CardPlayView


urlpatterns = patterns(
    '',
    url(r'^$', login_required(CardListView.as_view()), name='card_list'),
    url(r'^(?P<pk>\d+)/$', login_required(CardDetailView.as_view()), name='card_detail'),
    url(r'^(?P<pk>\d+)/play/$', login_required(CardPlayView.as_view()), name='card_play'),
    url(r'^print/list/$',
        login_required(CardListView.as_view(template_name='card/card_list_print_list.html')),
        name='card_list_print_list'),
    url(r'^print/all/$',
        user_passes_test(lambda user: user.is_staff)(CardListView.as_view(
            template_name='card/card_list_print_all.html')),
        name='card_list_print_all'))
