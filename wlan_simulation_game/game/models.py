from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from ..exceptions import WLANSimulationGameError


class PlayerManager(UserManager):
    """
    Custom manager to disable email as required field for superusers.
    """
    def create_superuser(self, *args, **kwargs):
        kwargs.setdefault('email')
        return super().create_superuser(*args, **kwargs)


class Player(AbstractUser):
    """
    Model for the player groups.
    """
    description = models.TextField(blank=True, verbose_name=ugettext_lazy('Description'))

    objects = PlayerManager()

    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('is_staff', 'username',)
        verbose_name = ugettext_lazy('Player')
        verbose_name_plural = ugettext_lazy('Players')

    @property
    def is_superuser(self):
        """
        Property of a player object. Returns the value of the is_staff
        database field. The is_superuser database field is ignored.
        """
        return self.is_staff

    @is_superuser.setter
    def is_superuser(self, value):
        """
        Setting values to the is_superuser database field is disabled.
        """
        pass

    @property
    def score(self):
        """
        Returns the actual score of the player according to all played cards.
        """
        from constance import config
        value_sum = self.cards_against_me.aggregate(models.Sum('value'))['value__sum']
        # value_sum = self.cards_against_me.filter(used=True).aggregate(models.Sum('value'))['value__sum']
        if value_sum is None:
            value_sum = 0
        return config.start_score + value_sum

    @property
    def playable_cards(self):
        """
        Returns the remaining number of playable cards of the player.
        """
        from constance import config
        return config.playable_cards - self.cards.count()
        # return config.playable_cards - self.cards.filter(used=True).count()

    @property
    def relative_score(self):
        """
        Returns 45/50 of the score. This is just for the bars in the template.
        """
        return self.score * 45 / 50


class Message(models.Model):
    """
    Model for messages between players.

    If the recepient is None, it means that it is a message to all players.
    """
    sender = models.ForeignKey(
        Player,
        related_name='sent_messages',
        verbose_name=ugettext_lazy('Sender'))
    recipient = models.ForeignKey(
        Player,
        null=True,
        related_name='received_messages',
        verbose_name=ugettext_lazy('Recipient'))
    subject = models.CharField(max_length=32, verbose_name=ugettext_lazy('Subject'))
    text = models.TextField(verbose_name=ugettext_lazy('Text'))
    printed = models.BooleanField(default=False, verbose_name=ugettext_lazy('Printed'))
    sending_time = models.TimeField(auto_now_add=True, verbose_name=ugettext_lazy('Sending Time'))

    class Meta:
        ordering = ('sender', 'recipient', 'sending_time')
        verbose_name = ugettext_lazy('Message')
        verbose_name_plural = ugettext_lazy('Messages')

    def save(self, *args, **kwargs):
        """
        Override to check that no one is sender and recipient at one time.
        """
        if self.sender == self.recipient:
            raise WLANSimulationGameError(_('The sender can not be saved as recipient.'))
        return super().save(*args, **kwargs)

    def __str__(self):
        """
        Method for representation.
        """
        return self.subject

    @models.permalink
    def get_absolute_url(self):
        """
        Returns the url to the detail view of the message.
        """
        return ('message_detail', [str(self.pk)])


class Interception(models.Model):
    """
    Model for an interception by one player against two others.
    """
    interceptor = models.ForeignKey(
        Player,
        verbose_name=ugettext_lazy('Interceptor'))
    message = models.ForeignKey(
        Message,
        verbose_name=ugettext_lazy('Message'))

    class Meta:
        unique_together = ('interceptor', 'message')
        verbose_name = ugettext_lazy('Interception')
        verbose_name_plural = ugettext_lazy('Interceptions')

    def save(self, *args, **kwargs):
        """
        Override to check that a player can only intercept messages of other
        players and only the allowed number of messages.
        """
        from constance import config
        if self.message.sender.is_staff:
            raise WLANSimulationGameError(_('You can not intercept messages from the game master.'))
        if (self.message.sender == self.interceptor or
                self.message.recipient == self.interceptor or
                self.message.recipient is None):
            raise WLANSimulationGameError(_('You can not intercept a message from or to yourself.'))
        if Interception.objects.filter(interceptor=self.interceptor).count() >= config.number_of_interceptions:
            raise WLANSimulationGameError(
                _('You can only intercept a total number of %d messages.') % config.number_of_interceptions)
        try:
            return_value = super().save(*args, **kwargs)
        except IntegrityError as error:
            if error.args[0] == 'UNIQUE constraint failed: game_interception.interceptor_id, game_interception.message_id':
                error_message = _('There is no new message you have not intercepted yet. Try again later.')
            else:
                error_message = error.args
            raise WLANSimulationGameError(error_message)
        return return_value

    def __str__(self):
        """
        Method for representation.
        """
        return '%s -- %s (%s to %s)' % (self.interceptor, self.message, self.message.sender, self.message.recipient)


def validate_not_zero(value):
    if value == 0:
        raise ValidationError(_('Zero is not allowed.'))


class Card(models.Model):
    """
    Model for good and bad cards the players can play.
    """
    PATH_COICES = (
        (0, ugettext_lazy('Bad path')),
        (1, ugettext_lazy('Path 1')),
        (2, ugettext_lazy('Path 2')),
        (3, ugettext_lazy('Path 3')))

    name = models.CharField(max_length=255, verbose_name=ugettext_lazy('Name'))
    description = models.TextField(blank=True, verbose_name=ugettext_lazy('Description'))
    playing_player = models.ForeignKey(
        Player, null=True, blank=True, related_name='cards',
        verbose_name=ugettext_lazy('Playing player'))
    receiving_player = models.ForeignKey(
        Player, null=True, blank=True, related_name='cards_against_me',
        verbose_name=ugettext_lazy('Receiving player'))
    value = models.IntegerField(validators=[validate_not_zero],
        verbose_name=ugettext_lazy('Value'))
    path = models.IntegerField(choices=PATH_COICES, verbose_name=ugettext_lazy('Path'))
    level = models.IntegerField(verbose_name=ugettext_lazy('Level'))
    bad_playing_player = models.ForeignKey(
        Player, null=True, blank=True, related_name='bad_cards',
        verbose_name=ugettext_lazy('Bad playing player'))
    bad_receiving_player = models.ForeignKey(
        Player, null=True, blank=True, related_name='bad_cards_against_me',
        verbose_name=ugettext_lazy('Bad receiving player'))

    class Meta:
        ordering = ('-path', 'level')
        verbose_name = ugettext_lazy('Card')
        verbose_name_plural = ugettext_lazy('Cards')

    def save(self, *args, **kwargs):
        """
        Checks that a player can not play more cards that his config limit
        allows.
        """
        if self.playing_player is not None:
            if self.playing_player.playable_cards <= 0:
                raise WLANSimulationGameError(_('%s can not play cards anymore.') % self.playing_player)
        return super().save(*args, **kwargs)

    def __str__(self):
        """
        Method for representation.
        """
        return self.name

    def clean(self):
        """
        Checks that a card is setup correctly.
        """
        if self.playing_player is None and self.receiving_player is not None:
            raise ValidationError(_('You need to set a playing player if you '
                'want to set a receiving player.'))
        if self.playing_player is not None and self.playing_player == self.receiving_player:
            raise ValidationError(_('The playing player can not be the receiving player.'))
        if self.value > 0:
            if self.path == 0:
                raise ValidationError(_('Do not set a positiv value if the '
                    'card does belong to the bad path.'))
        else:
            if self.path != 0:
                raise ValidationError(_('Do not set a negativ value if the '
                    'card does not belong to the bad path.'))
            if self.bad_playing_player is None or self.bad_receiving_player is None:
                raise ValidationError(_('The fields bad playing player and '
                    'bad receiving player are required for negativ cards.'))
            if self.playing_player is not None and self.playing_player != self.bad_playing_player:
                raise ValidationError(_('The bad card can only be played by '
                    'the bad playing player.'))
            if self.receiving_player is not None and self.receiving_player != self.bad_receiving_player:
                raise ValidationError(_('The bad card can only be played on '
                    'the bad receiving player.'))

    def is_played(self):
        """
        Returns True if the card is played and can not be play once again.
        """
        return self.playing_player is not None


class ConventOffer(models.Model):
    """
    Model for an offer in the convent.
    """
    offeror = models.ForeignKey(
        Player, related_name='from_offers',
        verbose_name=ugettext_lazy('Offeror'))
    acceptor = models.ForeignKey(
        Player, related_name='to_offers',
        verbose_name=ugettext_lazy('Acceptor'))
    offered_card = models.ForeignKey(
        Card, related_name='from_offers',
        verbose_name=ugettext_lazy('Offered Card'))
    card_in_return = models.ForeignKey(
        Card, null=True, blank=True, related_name='to_offers',
        verbose_name=ugettext_lazy('Card in return'))

    class Meta:
        unique_together = (('offeror', 'acceptor'),)
        verbose_name = ugettext_lazy('Offer')
        verbose_name_plural = ugettext_lazy('Offers')

    def __str__(self):
        """
        Method for representation.
        """
        return 'Offer: %(offeror)s – %(acceptor)s' % {'offeror': self.offeror, 'acceptor': self.acceptor}


# class Card(models.Model):
    # """
    # Model for a card that one player, the owner, can play with respect to
    # another player, the target.
    # """
    # name = models.CharField(max_length=255, verbose_name=ugettext_lazy('Name'))
    # description = models.TextField(blank=True, verbose_name=ugettext_lazy('Description'))
    # owner = models.ForeignKey(Player, related_name='cards', verbose_name=ugettext_lazy('Owner'))
    # target = models.ForeignKey(Player, related_name='cards_against_me', verbose_name=ugettext_lazy('Target'))
    # value = models.IntegerField(verbose_name=ugettext_lazy('Value'))
    # used = models.BooleanField(default=False, verbose_name=ugettext_lazy('Used'))

    # class Meta:
        # ordering = ('owner', 'target', 'value')
        # verbose_name = ugettext_lazy('Card')
        # verbose_name_plural = ugettext_lazy('Cards')

    # def save(self, *args, **kwargs):
        # """
        # Override to check that no one is owner and target at one time.
        # """
        # if self.owner == self.target:
            # raise WLANSimulationGameError(_('The owner can not be saved as target.'))
        # return super().save(*args, **kwargs)

    # def __str__(self):
        # """
        # Method for representation.
        # """
        # return self.name

    # def play(self):
        # """
        # Method to play a card. No check of permissions.
        # """
        # if self.used:
            # raise WLANSimulationGameError(_('You can not play this card any more. It is already used.'))
        # elif self.owner.playable_cards <= 0:
            # raise WLANSimulationGameError(_('The owner can not play cards anymore.'))
        # else:
            # # Everything is ok, the card can be played.
            # pass
        # self.used = True
        # self.save()
