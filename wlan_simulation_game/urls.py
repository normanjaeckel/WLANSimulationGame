#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^print/$',
        user_passes_test(lambda user: user.is_staff)(TemplateView.as_view(
            template_name='home_print.html')),
        name='home_print'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^player/', include('wlan_simulation_game.player.urls')),
    url(r'^card/', include('wlan_simulation_game.card.urls')),
    url(r'^message/', include('wlan_simulation_game.message.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
