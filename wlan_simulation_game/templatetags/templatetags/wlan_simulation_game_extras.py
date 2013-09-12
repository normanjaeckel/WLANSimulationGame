#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse

from constance import config


register = template.Library()


@register.simple_tag(takes_context=True)
def url_href_class_current(context, url_name):
    """
    This custom template tag checks whether the requested path starts with
    the given named url. It returns all attributes for the html a tag.
    """
    url = reverse(url_name)
    html_tag_attributes = 'href="%s"' % url
    if (context['request'].path.startswith(url) and
            (context['request'].path == '/' or not url == '/')):
        html_tag_attributes += ' class="current"'
    return html_tag_attributes


@register.filter
def rest_interceptions(count):
    """
    Returns the differenc between the maximum number of interceptions the the
    given value.
    """
    return config.number_of_interceptions - count
