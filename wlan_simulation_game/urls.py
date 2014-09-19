from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic

from .game import forms, models, views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Home and authentication
    url(r'^$',
        generic.TemplateView.as_view(template_name='home.html'),
        name='home'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$',
        'django.contrib.auth.views.logout_then_login',
        name='logout'),

    # Print views for staff users
    url(r'^print/introduction/$',
        user_passes_test(lambda user: user.is_staff)(generic.TemplateView.as_view(
            template_name='print_introduction.html')),
        name='print_introduction'),
    url(r'^print/access-data/$',
        user_passes_test(lambda user: user.is_staff)(generic.ListView.as_view(
            model=models.Player,
            template_name='print_access_data.html')),
        name='print_access_data'),
    url(r'^print/player/$',
        user_passes_test(lambda user: user.is_staff)(generic.ListView.as_view(
            queryset=models.Player.objects.filter(is_staff=False),
            template_name='print_player_list.html')),
        name='print_player_list'),
    url(r'^print/card/full/$',
        user_passes_test(lambda user: user.is_staff)(views.CardListView.as_view(
            template_name='print_card_list_full.html')),
        name='print_card_list_full'),
    url(r'^print/card/short/$',
        user_passes_test(lambda user: user.is_staff)(views.CardListView.as_view(
            template_name='print_card_list_short.html')),
        name='print_card_list_short'),

    # Player
    url(r'^player/$',
        login_required(generic.ListView.as_view(
            queryset=models.Player.objects.filter(is_staff=False))),
        name='player_list'),
    url(r'^player/(?P<pk>\d+)/$',
        login_required(generic.DetailView.as_view(
            queryset=models.Player.objects.filter(is_staff=False))),
        name='player_detail'),

    # Message
    url(r'^message/$',
        login_required(views.MessageListView.as_view()),
        name='message_list'),
    url(r'^message/not-printed/$',
        user_passes_test(lambda user: user.is_staff)(generic.ListView.as_view(
            queryset=models.Message.objects.filter(printed=False).order_by('sending_time'),
            template_name='game/message_list_not_printed.html')),
        name='message_list_not_printed'),
    url(r'^message/create/$',
        login_required(views.MessageCreateView.as_view()),
        name='message_create'),
    url(r'^message/(?P<pk>\d+)/$',
        login_required(views.MessageDetailView.as_view()),
        name='message_detail'),
    url(r'^message/(?P<pk>\d+)/print/$',
        user_passes_test(lambda user: user.is_staff)(views.MessagePrintView.as_view()),
        name='message_print'),
    url(r'^message/interception/$',
        login_required(views.InterceptionWizardView.as_view(
            [forms.InterceptionWizardFormOne, forms.InterceptionWizardFormTwo])),
        name='interception'),

    # Card
    url(r'^card/$',
        login_required(views.CardListView.as_view()),
        name='card_list'),
    url(r'^card/(?P<pk>\d+)/$',
        login_required(views.CardDetailView.as_view()),
        name='card_detail'),
    url(r'^card/(?P<pk>\d+)/play/$',
        user_passes_test(lambda user: user.is_staff)(views.CardPlayView.as_view()),
        name='card_play'),

    # Admin
    url(r'^admin/', include(admin.site.urls)))
