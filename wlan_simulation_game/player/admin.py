#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Player


admin.site.register(Player)
admin.site.unregister(Group)
