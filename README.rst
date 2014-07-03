======================
 WLAN Simulation Game
======================

A system for WLAN supported simulation games. It is optimized for 15 to 25
players in five groups.


Requirements
------------

You need a server with

* Python 2.7.x
* Virtual Python Environment builder 1.11.x (optional, but recommended)
* Django 1.5.8
* Constance – Dynamic Django settings 0.6 (Backend: Database)
* Actual webbrowser with support for HTML5 and CSS3

At least one player of each group of players needs a client computer with
an actual webbrowser. All client computers and the server need access to a
network, e. g. a WLAN.


Install
-------

This is only an example instruction for a Unix system where Python and Git
is already installed.

::

    $ git clone https://github.com/normanjaeckel/WLANSimulationGame.git  # You can also extract the downloaded compressed tar archive from GitHub instead of using git.

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

    $ python manage.py runserver --insecure 0.0.0.0:8000


Configuration
-------------

First an admin user and an user for each player character has to be setup
via the admin panel. After this, the player characters can be created and
connected to the before created users. All configuration values have to be
setup in the menu item Constance/Config. Last but not least all playable
cards with all texts, owners, targets and scores have to be entered.

Now you can print the cards, the list of all cards, the player
descriptions, the game introduction and an access data sheet and give them
to the players.

Every group of players gets its own cards (with scores), a list of all
cards (without scores), a list of all players with descriptions, a game
introduction and its access data sheet.

At the beginning of the game the configuration flag to allow writing
messages has to be activated by the game master. Now the players can
communicate and deal with the other groups. All messages have to be printed
for there is intentionally no possibility for the players to receive
messages via the interface. All played cards have to be marked as played
manually in the interface by the game master.


Example
-------

To load the data of the German example simulation game „Wissen ist Macht“,
install the programm as metioned above and run::

    $ python manage.py loaddata examples/example_game_de_1.json

To load the data of the German example simulation game „Jeder ist seines
Glückes ...“, install the programm as metioned above and run::

    $ python manage.py loaddata examples/example_game_de_2.json

The user name of the game master is `admin`. The password for of all users
is `default`. All passwords have to be changed before starting the game.
You might also want to change the header image by replacing the respective
file in `wlan_simulation_game/static/images`.


Questions
---------

If you have any questions, do not hesitate to write me an email to
wlansimulationgame [at] normanjaeckel.de.
