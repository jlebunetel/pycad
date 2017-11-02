#!/usr/bin/env python
# -*- coding: utf-8 -*-

# types de ligne
TYPE_DU_CALQUE = 'BYLAYER'
TYPE_DU_BLOC = 'BYBLOCK'
TYPE_CONTINU = 'CONTINUOUS'
TYPE_CACHE = 'CACHE'
TYPE_AXES = 'AXES'

# couleurs
COULEUR_DU_CALQUE = 256
COULEUR_DU_BLOC = 0
ROUGE = 1
JAUNE = 2
VERT = 3
CYAN = 4
BLEU = 5
MAGENTA = 6
BLANC = 7
GRIS = 8

# symétrie du texte
SYMETRIE_AUCUNE = '0'
SYMETRIE_HORIZONTALE = '2'
SYMETRIE_VERTICALE = '4'

# alignement horizontal du texte
GAUCHE = '0'
CENTRE = '1'
DROITE = '2'

# alignement vertical du texte
BASE = '0'
BAS = '1'
MILIEU = '2'
HAUT = '3'

# calques
CALQUE_DEFAULT = ['0', TYPE_CONTINU, BLANC]

# polylignes
OUVERTE = 0
FERMEE = 1

class Layer:
    def __init__(self, **kwargs):
        kwargs.setdefault('name', '0')
        kwargs['name'] = kwargs['name'].upper()
        kwargs.setdefault('linetype', TYPE_CONTINU)
        kwargs.setdefault('color', BLANC)

        self.name = kwargs['name']
        self.linetype = kwargs['linetype']
        self.color = kwargs['color']

    def __str__(self):
        return "layer [{0}, {1}, {2}]".format(self.name, self.linetype, self.color)

    def generate(self):
        text = '0' + '\n' + 'LAYER' + '\n'
        text+= '2' + '\n' + self.name + '\n'
        text+= '6' + '\n' + self.linetype + '\n'
        text+= '62' + '\n' + str(self.color) + '\n'
        text+= '70' + '\n' + '64' + '\n'
        return text

class Entity:
    def __init__(self, **kwargs):
        kwargs.setdefault('linetype', TYPE_DU_CALQUE)
        kwargs.setdefault('layer', Layer(name='0', linetype=TYPE_CONTINU, color=BLANC))
        kwargs.setdefault('color', COULEUR_DU_CALQUE)

        self.linetype = kwargs['linetype']
        self.layer = kwargs['layer']
        self.color = kwargs['color']

class Point(Entity):
    def __init__(self, **kwargs):
        kwargs.setdefault('x', 0)
        kwargs.setdefault('y', 0)
        kwargs.setdefault('z', 0)

        Entity.__init__(self, **kwargs)
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.z = kwargs['z']

    def generate(self):
        text = '0' + '\n' + 'POINT' + '\n'
        text+= '6' + '\n' + self.linetype + '\n'
        text+= '8' + '\n' + self.layer.name + '\n'
        text+= '10' + '\n' + str(self.x) + '\n'
        text+= '20' + '\n' + str(self.y) + '\n'
        text+= '30' + '\n' + str(self.z) + '\n'
        text+= '62' + '\n' + str(self.color) + '\n'
        return text

class Line(Entity):
    def __init__(self, **kwargs):
        kwargs.setdefault('start_point', Point())
        kwargs.setdefault('end_point', Point(x=1))

        Entity.__init__(self, **kwargs)
        self.start_point = kwargs['start_point']
        self.end_point = kwargs['end_point']

    def generate(self):
        text = '0' + '\n' + 'LINE' + '\n'
        text+= '6' + '\n' + self.linetype + '\n'
        text+= '8' + '\n' + self.layer.name + '\n'
        text+= '10' + '\n' + str(self.start_point.x) + '\n'
        text+= '20' + '\n' + str(self.start_point.y) + '\n'
        text+= '30' + '\n' + str(self.start_point.z) + '\n'
        text+= '11' + '\n' + str(self.end_point.x) + '\n'
        text+= '21' + '\n' + str(self.end_point.y) + '\n'
        text+= '31' + '\n' + str(self.end_point.z) + '\n'
        text+= '62' + '\n' + str(self.color) + '\n'
        return text

class Polyline(Entity):
    def __init__(self, **kwargs):
        kwargs.setdefault('flag', OUVERTE)
        kwargs.setdefault('start_width', 0.0)
        kwargs.setdefault('end_width', 0.0)
        kwargs.setdefault('bulge', 0.0)

        Entity.__init__(self, **kwargs)
        self.points = []
        self.flag = kwargs['flag']
        self.start_width = kwargs['start_width']
        self.end_width = kwargs['end_width']
        self.bulge = kwargs['bulge']

    def generate(self):
        text = '0' + '\n' + 'POLYLINE' + '\n'
        text+= '6' + '\n' + self.linetype + '\n'
        text+= '8' + '\n' + self.layer.name + '\n'
        text+= '40' + '\n' + str(self.start_width) + '\n' # épaisseur de départ
        text+= '41' + '\n' + str(self.end_width) + '\n' # épaisseur de fin
        text+= '62' + '\n' + str(self.color) + '\n'
        text+= '66' + '\n' + '1' + '\n'
        text+= '70' + '\n' + str(self.flag) + '\n'

        for point in self.points:
            text+= '0' + '\n' + 'VERTEX' + '\n'
            text+= '8' + '\n' + '0' + '\n'
            text+= '10' + '\n' + str(point.x) + '\n'
            text+= '20' + '\n' + str(point.y) + '\n'
            text+= '30' + '\n' + str(point.z) + '\n'
            text+= '42' + '\n' + str(self.bulge) + '\n' # courbure de l'arc : 0 = droit, 1 = demi-cercle

        text+= '0' + '\n' + 'SEQEND' + '\n'
        text+= '8' + '\n' + '0' + '\n'

        return text

    # fonction point
    def add_point(self,  point):
        self.points.append(point)
        return 0

class Rectangle(Polyline):
    def __init__(self, **kwargs):
        kwargs.setdefault('point_1', Point())
        kwargs.setdefault('point_3', Point(x=1, y=2))

        self.point_1 = kwargs['point_1']
        self.point_3 = kwargs['point_3']
        self.point_2 = Point(x=self.point_3.x, y=self.point_1.y, z=self.point_1.z)
        self.point_4 = Point(x=self.point_1.x, y=self.point_3.y, z=self.point_3.z)

        kwargs['flag'] = FERMEE
        Polyline.__init__(self, **kwargs)
        self.points = [self.point_1, self.point_2, self.point_3, self.point_4]

class Disk(Polyline):
    def __init__(self, **kwargs):
        kwargs.setdefault('center_point', Point())
        kwargs.setdefault('radius', 1.0)

        self.center_point = kwargs['center_point']
        self.radius = kwargs['radius']

        kwargs['flag'] = FERMEE
        kwargs['start_width'] = self.radius
        kwargs['end_width'] = self.radius
        kwargs['bulge'] = 1.0
        Polyline.__init__(self, **kwargs)
        point_A = Point(x=(self.center_point.x - self.radius / 2), y=self.center_point.y,  z=self.center_point.z)
        point_B = Point(x=(self.center_point.x + self.radius / 2), y=self.center_point.y,  z=self.center_point.z)
        self.points = [point_A, point_B]

class Circle(Entity):
    def __init__(self, **kwargs):
        kwargs.setdefault('center_point', Point())
        kwargs.setdefault('radius', 1.0)
        kwargs.setdefault('direction', Point(z=1))

        Entity.__init__(self, **kwargs)
        self.center_point = kwargs['center_point']
        self.radius = kwargs['radius']
        self.direction = kwargs['direction']

    def generate(self):
        text = '0' + '\n' + 'CIRCLE' + '\n'
        text+= '6' + '\n' + self.linetype + '\n'
        text+= '8' + '\n' + self.layer.name + '\n'
        text+= '10' + '\n' + str(self.center_point.x) + '\n'
        text+= '20' + '\n' + str(self.center_point.y) + '\n'
        text+= '30' + '\n' + str(self.center_point.z) + '\n'
        text+= '40' + '\n' + str(self.radius) + '\n'
        text+= '62' + '\n' + str(self.color) + '\n'
        text+= '210' + '\n' + str(self.direction.x) + '\n'
        text+= '220' + '\n' + str(self.direction.y) + '\n'
        text+= '230' + '\n' + str(self.direction.z) + '\n'
        return text

class Arc(Entity):
    def __init__(self, **kwargs):
        kwargs.setdefault('center_point', Point())
        kwargs.setdefault('radius', 1.0)
        kwargs.setdefault('direction', Point(z=1))
        kwargs.setdefault('start_angle', 0.0)
        kwargs.setdefault('end_angle', 45.0)

        Entity.__init__(self, **kwargs)
        self.center_point = kwargs['center_point']
        self.radius = kwargs['radius']
        self.direction = kwargs['direction']
        self.start_angle = kwargs['start_angle']
        self.end_angle = kwargs['end_angle']

    def generate(self):
        text = '0' + '\n' + 'ARC' + '\n'
        text+= '6' + '\n' + self.linetype + '\n'
        text+= '8' + '\n' + self.layer.name + '\n'
        text+= '10' + '\n' + str(self.center_point.x) + '\n'
        text+= '20' + '\n' + str(self.center_point.y) + '\n'
        text+= '30' + '\n' + str(self.center_point.z) + '\n'
        text+= '40' + '\n' + str(self.radius) + '\n'
        text+= '50' + '\n' + str(self.start_angle) + '\n'
        text+= '51' + '\n' + str(self.end_angle) + '\n'
        text+= '62' + '\n' + str(self.color) + '\n'
        text+= '210' + '\n' + str(self.direction.x) + '\n'
        text+= '220' + '\n' + str(self.direction.y) + '\n'
        text+= '230' + '\n' + str(self.direction.z) + '\n'
        return text

class Solid(Entity):
    def __init__(self, **kwargs):
        kwargs.setdefault('point_1', Point(x=0, y=0))
        kwargs.setdefault('point_2', Point(x=0, y=1))
        kwargs.setdefault('point_3', Point(x=1, y=1))
        kwargs.setdefault('point_4', Point(x=1, y=0))

        Entity.__init__(self, **kwargs)
        self.point_1 = kwargs['point_1']
        self.point_2 = kwargs['point_2']
        self.point_3 = kwargs['point_3']
        self.point_4 = kwargs['point_4']

    def generate(self):
        text = '0' + '\n' + 'SOLID' + '\n'
        text+= '6' + '\n' + self.linetype + '\n'
        text+= '8' + '\n' + self.layer.name + '\n'
        text+= '10' + '\n' + str(self.point_1.x) + '\n'
        text+= '20' + '\n' + str(self.point_1.y) + '\n'
        text+= '30' + '\n' + str(self.point_1.z) + '\n'
        text+= '11' + '\n' + str(self.point_2.x) + '\n'
        text+= '21' + '\n' + str(self.point_2.y) + '\n'
        text+= '31' + '\n' + str(self.point_2.z) + '\n'
        text+= '12' + '\n' + str(self.point_4.x) + '\n'
        text+= '22' + '\n' + str(self.point_4.y) + '\n'
        text+= '32' + '\n' + str(self.point_4.z) + '\n'
        text+= '13' + '\n' + str(self.point_3.x) + '\n'
        text+= '23' + '\n' + str(self.point_3.y) + '\n'
        text+= '33' + '\n' + str(self.point_3.z) + '\n'
        text+= '62' + '\n' + str(self.color) + '\n'
        return text

class Plein_rectangle(Solid):
    def __init__(self, **kwargs):
        kwargs.setdefault('point_1', Point())
        kwargs.setdefault('point_3', Point(x=3, y=2))

        self.point_1 = kwargs['point_1']
        self.point_3 = kwargs['point_3']
        self.point_2 = Point(x=self.point_3.x, y=self.point_1.y, z=self.point_1.z)
        self.point_4 = Point(x=self.point_1.x, y=self.point_3.y, z=self.point_3.z)

        kwargs['point_2'] = self.point_2
        kwargs['point_4'] = self.point_4
        Solid.__init__(self, **kwargs)

class Text(Entity):
    def __init__(self, **kwargs):
        kwargs.setdefault('start_point', Point())
        kwargs.setdefault('text', 'Hello world!')
        kwargs.setdefault('height', 5.0)
        kwargs.setdefault('horizontal_justification', GAUCHE)
        kwargs.setdefault('vertical_justification', BASE)
        kwargs.setdefault('scale_factor_width', 1.0)
        kwargs.setdefault('rotation', 0.0)
        kwargs.setdefault('oblique_angle', 0.0)
        kwargs.setdefault('generation_flags', SYMETRIE_AUCUNE)

        Entity.__init__(self, **kwargs)
        self.start_point = kwargs['start_point']
        self.text = kwargs['text']
        self.height = kwargs['height']
        self.horizontal_justification = kwargs['horizontal_justification']
        self.vertical_justification = kwargs['vertical_justification']
        self.scale_factor_width = kwargs['scale_factor_width']
        self.rotation = kwargs['rotation']
        self.oblique_angle = kwargs['oblique_angle']
        self.generation_flags = kwargs['generation_flags']

    def generate(self):
        text = '0' + '\n' + 'TEXT' + '\n'
        text+= '1' + '\n' + self.text + '\n'
        text+= '6' + '\n' + self.linetype + '\n'
        text+= '8' + '\n' + self.layer.name + '\n'
        text+= '10' + '\n' + str(self.start_point.x) + '\n'
        text+= '20' + '\n' + str(self.start_point.y) + '\n'
        text+= '30' + '\n' + str(self.start_point.z) + '\n'
        text+= '11' + '\n' + str(self.start_point.x) + '\n'
        text+= '21' + '\n' + str(self.start_point.y) + '\n'
        text+= '31' + '\n' + str(self.start_point.z) + '\n'
        text+= '40' + '\n' + str(self.height) + '\n'
        text+= '41' + '\n' + str(self.scale_factor_width) + '\n'
        text+= '50' + '\n' + str(self.rotation) + '\n'
        text+= '51' + '\n' + str(self.oblique_angle) + '\n'
        text+= '62' + '\n' + str(self.color) + '\n'
        text+= '71' + '\n' + self.generation_flags + '\n'
        text+= '72' + '\n' + self.horizontal_justification + '\n'
        text+= '73' + '\n' + self.vertical_justification + '\n'
        return text

class Drawing:
    def __init__(self, **kwargs):
        self.linetypes = []
        self.layers = [Layer(name='0', linetype=TYPE_CONTINU, color=BLANC),]
        self.entities = []

    def __str__(self):
        return "Drawing object"

    def add_layer(self, layer):
        self.layers.append(layer)
        return 0

    # fonction point
    def add_entity(self,  entity):
        self.entities.append(entity)
        return 0


    def generate(self, **kwargs):
        kwargs.setdefault('file_name', 'export')

        # ouverture du fichier
        fichier = open(kwargs['file_name'] + '.dxf','w')

        # début de la définition des tables
        fichier.write('0' + '\n' + 'SECTION' + '\n')
        fichier.write('2' + '\n' + 'TABLES' + '\n')


        # début de la définition des styles de ligne
        fichier.write('0' + '\n' + 'TABLE' + '\n')
        fichier.write('2' + '\n' + 'LTYPE' + '\n')
        fichier.write('70' + '\n' + '3' + '\n')

        '''self.add_linetype(
            type=TYPE_CONTINU,
            description='Solid _________________________________________'),


        for linetype in linetypes:
            fichier.write(linetype)
            '''

        fichier.write('0' + '\n' + 'LTYPE' + '\n')
        fichier.write('2' + '\n' + TYPE_CONTINU + '\n')
        fichier.write('3' + '\n' + 'Solid _________________________________________' + '\n')
        fichier.write('70' + '\n' + '64' + '\n')
        fichier.write('72' + '\n' + '65' + '\n')
        fichier.write('73' + '\n' + '0' + '\n')
        fichier.write('40' + '\n' + '0.0' + '\n')

        fichier.write('0' + '\n' + 'LTYPE' + '\n')
        fichier.write('2' + '\n' + TYPE_CACHE + '\n')
        fichier.write('3' + '\n' + 'Cache __ __ __ __ __ __ __ __ __ __ __ __ __ __' + '\n')
        fichier.write('70' + '\n' + '0' + '\n')
        fichier.write('72' + '\n' + '65' + '\n')
        fichier.write('73' + '\n' + '2' + '\n')
        fichier.write('40' + '\n' + '0.375' + '\n')
        fichier.write('49' + '\n' + '0.25' + '\n')
        fichier.write('49' + '\n' + '-0.125' + '\n')

        fichier.write('0' + '\n' + 'LTYPE' + '\n')
        fichier.write('2' + '\n' + TYPE_AXES + '\n')
        fichier.write('3' + '\n' + 'Centre ____ _ ____ _ ____ _ ____ _ ____ _ ____' + '\n')
        fichier.write('70' + '\n' + '0' + '\n')
        fichier.write('72' + '\n' + '65' + '\n')
        fichier.write('73' + '\n' + '4' + '\n')
        fichier.write('40' + '\n' + '2.0' + '\n')
        fichier.write('49' + '\n' + '1.25' + '\n')
        fichier.write('49' + '\n' + '-0.25' + '\n')
        fichier.write('49' + '\n' + '0.25' + '\n')
        fichier.write('49' + '\n' + '-0.25' + '\n')

        # fin de la définition des styles de ligne
        fichier.write('0' + '\n' + 'ENDTAB' + '\n')


        # début de la définition des calques
        fichier.write('0' + '\n' + 'TABLE' + '\n')
        fichier.write('2' + '\n' + 'LAYER' + '\n')
        fichier.write('70' + '\n' + '4' + '\n')

        '''
        for calque in calques:
            fichier.write('0' + '\n' + 'LAYER' + '\n')
            fichier.write('2' + '\n' + calque[0] + '\n')
            fichier.write('6' + '\n' + calque[1] + '\n')
            fichier.write('62' + '\n' + str(calque[2]) + '\n')
            fichier.write('70' + '\n' + '64' + '\n')
            '''

        for layer in self.layers:
            fichier.write(layer.generate())

        # fin de la définition des calques
        fichier.write('0' + '\n' + 'ENDTAB' + '\n')


        # fin de la définition des tables
        fichier.write('0' + '\n' + 'ENDSEC' + '\n')

        # début de la définition des entités
        fichier.write('0' + '\n' + 'SECTION' + '\n')
        fichier.write('2' + '\n' + 'ENTITIES' + '\n')

        # fermeture du fichier dxf
        #fichier.close()

        for entity in self.entities:
            fichier.write(entity.generate())



        # ajout à la fin du fichier dxf du pied de page

        # ouverture du fichier
        ##fichier = open(chemin,'a')

        # fin de la définition des entités
        fichier.write('0' + '\n' + 'ENDSEC' + '\n')

        # fin du fichier
        fichier.write('0' + '\n' + 'EOF')

        # fermeture du fichier dxf
        fichier.close()

        # fin de la fonction
        return 0
