from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PlayerConfig(AppConfig):
    name = 'wlan_simulation_game.player'
    verbose_name = ugettext_lazy('Player')
