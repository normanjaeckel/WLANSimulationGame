#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^player/', include('wlan_simulation_game.player.urls')),
    url(r'^card/', include('wlan_simulation_game.card.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
