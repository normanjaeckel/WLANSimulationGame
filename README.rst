======================
 WLAN Simulation Game
======================

A system for WLAN supported simulation games for 15 to 25 players in five
groups.


Requirements
------------

You need a server with

* Python 2.7.x
* Virtual Python Environment builder 1.7.x (optional, but recommended)
* Django 1.5.2
* Constance – Dynamic Django settings 0.6 (Backend: Database)
* Actual webbrowser with support for HTML5 and CSS3

At least one player of each group of players needs a client computer with
an actual webbrowser. All client computers and the server need access to a
network, e. g. a WLAN.


Install
-------

::

    $ git clone https://github.com/normanjaeckel/WLANSimulationGame.git

    $ cd WLANSimulationGame

    $ virtualenv .virtualenv

    $ source .virtualenv/bin/activate  # On Windows use: .virtualenv\Scripts\activate

    $ python --version  # Ensure, that this returns Python 2.7.x

    $ pip install -r requirements.txt

    $ python helper_script.py --create-settings

    $ python manage.py syncdb


Start
-----

::

    $ python manage.py runserver 0.0.0.0:8000


Configuration
-------------

First an admin user and an user for each player character has to be setup
via the admin menu. After this, the player characters can be created and
connected to the before created users. Also all configuration values have
to be setup under the menu item Constance/Config. Last but not least all
playable cards with all texts, owners, targets and scores have to be entered.

At the beginning of the game the configuration flag to allow writing
messages has to be activated by the game master. All messages have to be
printed for there is intentionally no possibility for the players to
receive messages via the interface. All played cards have to be marked as
played manually in the interface by the game master.


Example
-------

To load the date of the German example simulation game, install the
programm as metioned above and run::

    $ python manage.py loaddata examples/example_game_de.json

The user name of the game master is `admin`. The password for of all users
is `default`. All passwords have to be changed before starting the game.
