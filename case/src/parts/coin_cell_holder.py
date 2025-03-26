from build123d import *
from copy import deepcopy

__SOLDER_TOL = 1.4*MM

__hole = Circle(1.2)

__holes = Pos(7.9, 0) * __hole + Pos(-12.1, 0) * __hole
solder_gap = extrude(__holes, -__SOLDER_TOL)


__HOUSING_DIMS = (24*MM, 22*MM, 7.6*MM)
__HOUSING_WITH_TOLS = (24.4*MM, 22.4*MM, 7.8*MM)

__SHELL_THICKNESS = 0.8

housing = Box(__HOUSING_DIMS[1]/2+2, 8, __HOUSING_DIMS[2], align=(Align.MAX, Align.CENTER, Align.MIN)) + \
        Pos(-2,0,0) * extrude(SlotCenterToCenter(4,__HOUSING_DIMS[1]), __HOUSING_DIMS[2])
housing2 = Box(__HOUSING_DIMS[1]/2+2, 8, __HOUSING_DIMS[2], align=(Align.MAX, Align.CENTER, Align.MIN)) + \
        Pos(-0.5,0,0) * extrude(SlotCenterToCenter(1,__HOUSING_DIMS[1]), __HOUSING_DIMS[2])
housing= offset(housing, .2, kind=Kind.INTERSECTION).split(Plane.XY)
housing2= offset(housing2, .2, kind=Kind.INTERSECTION).split(Plane.XY)

surface_points = [(-2,0),(-2, 4.6), (-0.6, 7.6), (3.7+7.05-5.96, 7.6),   
    (5.5, 4.6), (24-5.5, 4.6), (24-3, 5.6),(25, 5.6), (25,0)]
shell_face = Pos(-13,-11) * Rot(90,0,0) * make_face(Polyline(surface_points).close())
__housing_wave = extrude(shell_face, -22)
housing_cutter = offset(__housing_wave, .2, kind=Kind.INTERSECTION).split(Plane.XY)
housing_all= housing + offset(Box(__HOUSING_DIMS[1]/2+5, 8, __HOUSING_DIMS[2], align=(Align.MAX, Align.CENTER, Align.MIN)),.2,kind=Kind.INTERSECTION).split(Plane.XY)\
    + Pos(-16.2,0) * Cylinder(4.2,7.8,align=(Align.CENTER, Align.CENTER, Align.MIN))
housing_all2= housing2 + offset(Box(__HOUSING_DIMS[1]/2+5, 8, __HOUSING_DIMS[2], align=(Align.MAX, Align.CENTER, Align.MIN)),.2,kind=Kind.INTERSECTION).split(Plane.XY)\
    + Pos(-16.2,0) * Cylinder(4.2,7.8,align=(Align.CENTER, Align.CENTER, Align.MIN))
shell = offset(housing_all, .8, kind=Kind.INTERSECTION)
housing_cut= housing_all2.intersect(housing_cutter)
#shell= shell.intersect(housing_cutter2)
shell = split(shell, Plane.XY.offset(4))
shell -= housing_cut
shell += extrude(shell.faces().sort_by(Axis.Z)[-1], 0.6)
shell= chamfer(shell.edges().group_by(Axis.Z)[-1], 3.4,2)
shell -= Pos(-2, 0, 9.2) * extrude(SlotCenterToCenter(4,7), -1.01)
shell= chamfer(shell.edges().group_by(Axis.Z)[-1].sort_by_distance((0,0,0))[:4], 1.5,1)

if __name__ == '__main__': 
    from ocp_vscode import *
    show_all()
