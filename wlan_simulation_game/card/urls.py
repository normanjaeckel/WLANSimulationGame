#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView

from .models import Card
from .views import CardDetailView, CardPlayView


urlpatterns = patterns(
    '',
    url(r'^$', login_required(ListView.as_view(model=Card)), name='card_list'),
    url(r'^(?P<pk>\d+)/$', login_required(CardDetailView.as_view()), name='card_detail'),
    url(r'^(?P<pk>\d+)/play/$', login_required(CardPlayView.as_view()), name='card_play'),
    url(r'^print/list/$',
        login_required(ListView.as_view(
            model=Card,
            template_name='card/card_list_print_list.html')),
        name='card_list_print_list'),
    url(r'^print/all/$',
        user_passes_test(lambda user: user.is_staff)(ListView.as_view(
            model=Card,
            template_name='card/card_list_print_all.html')),
        name='card_list_print_all'),
)
