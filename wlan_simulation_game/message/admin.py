#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Message


admin.site.register(Message)
