from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class GameAppConfig(AppConfig):
    name = 'wlan_simulation_game.game'
    verbose_name = ugettext_lazy('Game')
