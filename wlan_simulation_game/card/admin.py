#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'target', 'value', 'used')


admin.site.register(Card, CardAdmin)
