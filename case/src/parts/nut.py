from build123d import *

__NUT_SIDES = 6
#tolerances already included
__NUT_EDGE_DIST = 4.5
__NUT_HEIGHT = 1.7

nut_cut = Rot(0,0,90) *RegularPolygon(radius=__NUT_EDGE_DIST/2,major_radius=False, side_count=__NUT_SIDES)
nut_cut = extrude(nut_cut, __NUT_HEIGHT)
if __name__ == '__main__':
    from ocp_vscode import *
    show_object(nut_cut, name="Nut Cutout")
