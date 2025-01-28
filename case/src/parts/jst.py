from build123d import *

__SOLDER_TOL = 1.4*MM


__BOX_DIMS = (8.9*MM,15*MM,4.6*MM)

solder_gap = Pos(2, 0) * Box(6, 2, __SOLDER_TOL, align=(Align.CENTER,Align.CENTER,Align.MAX))
box = Pos(-2.45, 1.85) * Box(*__BOX_DIMS,align=(Align.MIN,Align.MAX,Align.MIN))

__hollow_points = [
    (0, 0),
    (0, 19.5),
    (-3.5, 19.5),
    (-3.5, 19.5 + 6),
    (-3.5-19.05, 19.05 + 6),
    (-3.5-19.05, 19.05 + 6-2),
    (-3.5-19.05-10.48, 19.05 + 6-2),
    (-3.5-19.05-10.48, 0),
]
__hollow_face = Pos(13.51, -13) * make_face(Polyline(__hollow_points, close=True))
__hollow_face= offset(fillet(__hollow_face.vertices().group_by(Axis.Y)[0][-1], 6.66),-2)
hollow = extrude(__hollow_face, 5)


if __name__ == '__main__':
    from ocp_vscode import *
    show_all()
