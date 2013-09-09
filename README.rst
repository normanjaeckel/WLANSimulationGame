======================
 WLAN Simulation Game
======================

Ein System für WLAN-gestützte Planspiele für 15 bis 25 Personen.


Voraussetzungen
---------------

* Ein Server mit

  * Python 2.7.x mit Virtual Python Environment builder 1.7.x
  * Django 1.5.2
  * Constance – Dynamic Django settings 0.6 (Backend: Database)
  * Aktueller Browser mit Unterstützung für HTML5 und CSS3

* Mindestens ein Computer für jede Spielergruppe mit aktuellem Browser
* Zugang aller Computer zu einem Netzwerk, zum Beispiel ein eigenes WLAN


Installation
------------

::

    $ git clone https://github.com/normanjaeckel/wlan-simulation-game.git

    $ cd wlan-simulation-game

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


Einrichtung
-----------

Zusätzlich zum Administratorbenutzer muss über das Administrationsmenü für
jede Spielfigur zunächst ein Benutzer mit Benutzername und Passwort
angelegt werden. Danach können die Spieler angelegt und mit den jeweiligen
Benutzern verbunden werden. Weiterhin müssten unter dem Menüpunkt
Constance/Config alle allgemeinen Einstellungen vorgenommen werden.
Schließlich müssen alle Spielkarten mit den jeweiligen Texten, Besitzern
und Zielen sowie Punkten eingegeben werden. Zu Spielbeginn wird im
Menüpunkt Constance/Config das Schreiben von Nachrichten freigeschaltet. Am
Spielende kann dort das Schreiben von Nachrichten wieder deaktiviert
werden. Alle geschriebenen Nachrichten müssen ausgedruckt und persönlich
überbracht werden. Die Spieler haben keine Möglichkeit, über das Interface
Nachrichten zu empfangen. Alle von den Spielern mündlich gespielten Karten
werden durch die Spielleitung im Interface als ausgespielt markiert.


Beispiel
--------

Um die Daten eines Beispiel-Planspiels zu laden, geben Sie nach der
Installation ein::

    $ python manage.py loaddata example/example_game_de.json

Der Benutzername des Administrators lautet `admin`. Die Passwörter aller
Benutzer lauten `default`. Alle Passwörter müssen vor Spielbeginn geändert
werden.
