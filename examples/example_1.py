#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycad.main import *

dessin = Drawing()

gravure = Layer(name='marquage', linetype='CONTINUOUS', color=3)
dessin.add_layer(gravure)


espacement = 0.25
largeur = 30
hauteur = 30
decalage = 40

hauteur_texte = 2.5

for k in range(1, 11):
    dessin.add_entity(Rectangle(
        point_1=Point(x=0, y=(k * decalage)),
        point_3=Point(x=largeur, y=(k * decalage + hauteur)),
        ))

    dessin.add_entity(Text(
        start_point=Point(x=(largeur / 2), y=(k * decalage + hauteur + hauteur_texte)),
        text=str(k * espacement),
        height=hauteur_texte,
        horizontal_justification='1',
        ))

    for i in range(0, 1+int(largeur / (k * espacement))):
        dessin.add_entity(Line(start_point=Point(x=(i * k * espacement), y=(k * decalage)), end_point=Point(x=(i * k * espacement), y=(k * decalage + hauteur)), layer=gravure))

dessin.generate(file_name='dessin')
