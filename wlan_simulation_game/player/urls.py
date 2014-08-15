from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import DetailView, ListView

from .models import Player

urlpatterns = patterns(
    '',
    url(r'^$',
        login_required(ListView.as_view(
            queryset=Player.objects.filter(is_staff=False))),
        name='player_list'),
    url(r'^(?P<pk>\d+)/$',
        login_required(DetailView.as_view(
            queryset=Player.objects.filter(is_staff=False))),
        name='player_detail'),
    url(r'^print/$',
        user_passes_test(lambda user: user.is_staff)(ListView.as_view(
            queryset=Player.objects.filter(is_staff=False),
            template_name='player/player_list_print.html')),
        name='player_list_print'))
