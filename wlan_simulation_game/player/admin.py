#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('character', 'score', 'playable_cards')


admin.site.register(Player, PlayerAdmin)
admin.site.unregister(Group)
