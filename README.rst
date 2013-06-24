======================
 WLAN Simulation Game
======================

Ein System für WLAN-gestützte Planspiele für 15 bis 25 Personen.


Voraussetzungen
---------------

* Ein Server mit
  * Python 2.7 mit Virtual Python Environment builder 1.7
  * Django 1.5
  * Constance – Dynamic Django settings 0.6 (Backend: Database)
  * Aktueller Browser mit Unterstützung für HTML5 und CSS3
* Mindestens ein Computer für jede Spielergruppe mit aktuellem Browser
* Zugang aller Computer zu einem Netzwerk, z. B. ein eigenes WLAN


Installation
------------

$ git clone https://github.com/normanjaeckel/wlan-simulation-game.git

$ cd wlan-simulation-game

$ virtualenv .virtualenv

$ source .virtualenv/bin/activate

$ pip install Django==1.5.1 django_constance[database]==0.6

$ python manage.py syncdb


Start
-----

$ python manage.py runserver 0.0.0.0:8000
