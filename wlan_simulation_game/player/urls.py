#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, DetailView

from .models import Player


urlpatterns = patterns(
    '',
    url(r'^$', login_required(ListView.as_view(model=Player)), name='player_list'),
    url(r'^(?P<pk>\d+)/$', login_required(DetailView.as_view(model=Player)), name='player_detail'),
    url(r'^print/$',
        user_passes_test(lambda user: user.is_staff)(ListView.as_view(
            model=Player,
            template_name='player/player_list_print.html')),
        name='player_list_print'))
