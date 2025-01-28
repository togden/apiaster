from build123d import *


__outline = Wire.combine((Curve() + [
    Line((-4.574, -1.3), (-4.574, 1.3)),
    Line((-2.304, -1.3), (-4.574, -1.3)),
    Line((-2.304, -1.3), (-2.304, -1.5)),
    Line((-2.304, 1.3), (-4.574, 1.3)),
    Line((-2.304, 1.55), (-2.304, 1.3)),
    Line((-2.304, 1.55), (-1.504, 2.35)),
    Line((-1.504, -2.3), (-2.304, -1.5)),
    Line((-1.504, -2.3), (0.296, -2.3)),
    Line((-1.504, 2.35), (1.646, 2.35)),
    Line((2.446, 1.55), (1.646, 2.35)),
    Line((2.446, 1.55), (2.446, 1.2)),
    Line((2.451444, -3.79207), (2.456307, -3.79202)),
    Line((3.446, 0.2), (6.446, 0.2)),
    Line((7.246, -4.45), (3.396, -4.45)),
    Line((7.246, -3.5), (7.246, -4.45)),
    Line((7.246, -3.5), (9.6, -3.5)),
    Line((7.246, -0.9), (9.6, -0.9)),
    Line((7.246, -0.6), (7.246, -0.9)),
    Line((9.6, -0.9), (9.6, -3.5)),
    ThreePointArc((2.446, 1.2), (2.738893, 0.492893), (3.446, 0.2)),
    ThreePointArc((2.451444, -3.79207), (1.573272, -2.757765),
                  (0.295999, -2.300001)),
    ThreePointArc((2.456307, -3.79202), (2.822423, -4.269152), (3.396, -4.45)),
    ThreePointArc((7.246, -0.6), (7.011685, -0.034315), (6.446, 0.2))
]).wires(), tol=0.05*MM)

__face = make_face(__outline)

HOTSWAP_HEIGHT = 1.9*MM

component = extrude(__face, 1.85*MM)
component_with_tolerance = extrude(offset(__face, amount=0.4 * MM), -HOTSWAP_HEIGHT)

__circles = Pos(-5.5, 0) * Circle(2.2/2*MM) + \
    Circle(5.4/2*MM) + Pos(5.5, 0) * Circle(2.2/2*MM)
__cyls = extrude(__circles, -1.4*MM)
hotswap = Rot(0,0,180) * (__cyls + Pos(0, 5.95) * component_with_tolerance)

if __name__ == '__main__':
    from ocp_vscode import *
    show_object(component, name="CPG135001S30")
    show_object(component_with_tolerance,
                name="CPG135001S30 cutout with tolerance")
    show_object(hotswap, name="ChocV12_hotswap")
