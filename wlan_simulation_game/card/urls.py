#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from .models import Card
from .views import CardDetailView


urlpatterns = patterns(
    '',
    url(r'^$', login_required(ListView.as_view(model=Card)), name='card_list'),
    url(r'^(?P<pk>\d+)/$', login_required(CardDetailView.as_view()), name='card_detail'),
    #  url(r'^(?P<pk>\d+)/direktspielen/$', 'Planspiel_Glueck.karten.views.direkt_spielen', name='karten-direkt-spielen'),
    #  url(r'^drucken/$', 'Planspiel_Glueck.karten.views.drucken', name='karten-drucken'),
)
