#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect  # , HttpResponse
from django.views.generic import DetailView

from .models import Card

#~ from django.contrib.auth.decorators import permission_required
#~ from Planspiel_Glueck.karten.models import Karte
#~ #from Planspiel_Glueck.spieler.models import Spieler
#~
#~ from reportlab.pdfgen import canvas
#~ from reportlab.lib.units import cm
#~ from reportlab.platypus import Paragraph, Frame
#~ from reportlab.lib.styles import StyleSheet1, ParagraphStyle


class CardDetailView(DetailView):
    """
    View zur Anzeige einer eigenen Aktionskarte, abgeleitet von einer GenericView
    >is_staff< kann jede Karte sehen
    URL: /karten/pk mit variablem pk
    Antwort: 200 oder 302 nach /karten/ mit messages.error
    """
    model = Card

    def dispatch(self, request, *args, **kwargs):
        dispatch = super(CardDetailView, self).dispatch(request, *args, **kwargs)
        if request.user.is_staff or request.user.player == self.object.owner:
            return dispatch
        else:
            messages.error(request, 'Sie sind nicht Inhaber dieser Karte.')
            return HttpResponseRedirect(reverse('card_list'))

#~
#~ @permission_required('karten.can_play')
#~ def direkt_spielen(request, pk):
    #~ """
    #~ Eigene View zum direkten Spielen einer Karte auf den Zielspieler
    #~ URL: /karten/pk/direktspielen mit variabler pk
    #~ Ziel: /karten/ oder /karten/pk/ mit messages.error oder messages.success
    #~ """
    #~ try:
        #~ k = Karte.objects.get(pk=pk)
    #~ except Karte.DoesNotExist:
        #~ messages.error(request, 'Karte exisitiert nicht.')
        #~ return HttpResponseRedirect(reverse('karten-liste'))
    #~ if k.inhaber.kartenspielbar <= 0:
        #~ messages.error(request, 'Der Inhaber kann keine weiteren Karten ausspielen.')
        #~ return HttpResponseRedirect(reverse('karten-liste'))
    #~ try:
        #~ k.spielen()
    #~ except StandardError:
        #~ messages.error(request, 'Karte kann nicht ausgespielt werden. Die Karte ist bereits verbraucht.')
        #~ return HttpResponseRedirect(reverse('karten-liste'))
    #~ else:
        #~ messages.success(request, 'Karte wurde erfolgreich gespielt.')
        #~ return HttpResponseRedirect(reverse('karten-liste'))
#~
#~
#~ @permission_required('karten.can_print')
#~ def drucken(request):
    #~ """
    #~ View zur Generierung der Pdf für alle Karten
    #~ """
    #~ # Create the HttpResponse object with the appropriate PDF headers.
    #~ response = HttpResponse(mimetype='application/pdf')
    #~ response['Content-Disposition'] = 'attachment; filename=Planspiel_Glueck_Karten.pdf'
#~
    #~ # Create the PDF object, using the response object as its "file."
    #~ p = canvas.Canvas(response)
#~
    #~ # Draw things on the PDF. Here's where the PDF generation happens.
    #~ # See the ReportLab documentation for the full list of functionality.
    #~ # set stylesheets
    #~ stylesheet = StyleSheet1()
    #~ stylesheet.add(ParagraphStyle(name = 'Normal',
                              #~ fontName = 'Helvetica',
                              #~ fontSize = 26,
                              #~ leading = 30,
                              #~ spaceBefore = 20)
               #~ )
    #~ stylesheet.add(ParagraphStyle(name = 'Heading',
                              #~ fontName = 'Helvetica',
                              #~ fontSize = 44,
                              #~ leading = 49,
                              #~ spaceAfter = 25)
               #~ )
    #~ stylesheet.add(ParagraphStyle(name = 'Persons',
                              #~ fontName = 'Courier',
                              #~ fontSize = 20,
                              #~ leading = 24,
                              #~ spaceAfter = 10)
               #~ )
#~
    #~ for k in Karte.objects.all():
        #~ text1 = Paragraph(k.kartenname, stylesheet['Heading'])
        #~ text2 = Paragraph('Inhaber: ' + k.inhaber.figurname, stylesheet['Persons'])
        #~ text3 = Paragraph('Ziel: ' + k.ziel.figurname, stylesheet['Persons'])
        #~ text4 = Paragraph('Punkte: ' + str(k.wert), stylesheet['Persons'])
        #~ text5 = Paragraph(k.beschreibung, stylesheet['Normal'])
        #~ story = []
        #~ story.append(text1)
        #~ story.append(text2)
        #~ story.append(text3)
        #~ story.append(text4)
        #~ story.append(text5)
        #~ f = Frame(3*cm, 4*cm, 15*cm, 21*cm)
        #~ f.addFromList(story,p)
        #~ p.showPage()
    #~ p.save()
    #~ # Close the PDF object cleanly, and we're done.
    #~ #p.showPage()
    #~ #p.save()
    #~ return response
