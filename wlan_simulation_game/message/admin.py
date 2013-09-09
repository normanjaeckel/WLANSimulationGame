#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Message, Interception


admin.site.register(Message)
admin.site.register(Interception)
