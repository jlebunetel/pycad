#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycad.main import *


dessin = Drawing()

calque_kiki = Layer(name='kiki', linetype='AXES', color=2)
dessin.add_layer(calque_kiki)

print(dessin)

point = Point(layer=calque_kiki, x=9.5, y=4)
dessin.add_entity(point)

for i in range(10):
    for j in range(5):
        dessin.add_entity(Point(x=i, y=j, color=(i * j)))

dessin.add_entity(Line(start_point=point, layer=calque_kiki))

poly = Polyline(linetype='AXES', color=3, flag=1, bulge=0.3, start_width=0.5)
for i in range(10):
    poly.add_point(Point(x=i, y=i**2))
dessin.add_entity(poly)

dessin.add_entity(Rectangle())

dessin.add_entity(Disk(center_point=Point(x=-5, y=-7), radius=4.2))

dessin.add_entity(Circle(center_point=Point(x=-12, y=9)))

dessin.add_entity(Arc(radius=4.25, center_point=Point(x=-15, y=-30)))

dessin.add_entity(Solid())

dessin.add_entity(Plein_rectangle())

dessin.add_entity(Text())

dessin.generate(file_name='dessin')
for layer in dessin.layers:
    print(layer)
