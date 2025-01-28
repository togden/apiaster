from build123d import *


__outline = Wire.combine((Curve() + [
    Line((-6.085176, 1.30022),(-8.685176, 1.30022),),
    Line((-8.685176, 1.30022), (-8.685176, 3.75022)),
    Line((-8.685176, 3.75022), (-6.085176, 3.75022)),
    Line((-6.085176, 3.75022), (-6.085176, 4.75022)),
    ThreePointArc((-6.085176, 4.75022),(-5.4994, 6.1644),(-4.085176, 6.75022)),
    Line((-4.085176, 6.75022), (4.864824, 6.75022)),
    Line((4.864824, 6.75022), (4.864824, 6.32022)),
    Line((4.864824, 6.32022), (7.414824, 6.32022)),
    Line((7.414824, 6.32022), (7.414824, 3.87022)),
    Line((7.414824, 3.87022), (4.864824, 3.87022)),
    Line((4.864824, 3.87022), (4.864824, 2.70022)),
    Line((4.864824, 2.70022), (-0.2, 2.70022)),
    ThreePointArc((-0.2, 2.70022),(-1.6705, 2.1834),(-2.494322, 0.86022)),
    Line((-2.494322, 0.86022), (-6.085176, 0.86022)),
    Line((-6.085176, 0.86022),(-6.085176, 1.30022)),
]).wires(), tol=0.05*MM)

face = make_face(__outline)

HOTSWAP_HEIGHT = 1.9*MM

component = extrude(face, 1.85*MM)
component_with_tolerance = extrude(offset(face, amount=0.4 * MM), -HOTSWAP_HEIGHT)

__circles = Pos(-5.08, 0) * Circle(1.75/2*MM) + \
    Circle(3.9878/2*MM) + Pos(5.08, 0) * Circle(1.75/2*MM)
__cyls = extrude(__circles, -1.4*MM)
hotswap = Rot(0,0,180) * (__cyls + component_with_tolerance)

if __name__ == '__main__':
    from ocp_vscode import *
    show_all()
