from build123d import *

__INNER_D = 46
__OUTER_D = 56
__PUCK_D = 42
__PUCK_THICKNESS = 20
__SCREW_D = 4.5
__SCREW_HEAD_THICKNESS = 1.5
__THICKNESS = 0.6
__TOL = 0.2

magsafe_thickness_with_tol = __THICKNESS + __TOL

al = (Align.CENTER,Align.CENTER,Align.MAX)

magsafe = Cylinder(__OUTER_D/2 + __TOL, __THICKNESS + __TOL, align=al) -\
     Cylinder(__INNER_D/2 + __TOL, __THICKNESS + __TOL, align=al)


puck = Cylinder(__PUCK_D/2, __PUCK_THICKNESS + __TOL, align=al)
puck +=  [Rot(0,0,90*i)* Pos(19.05,0) for i in range(4)]  * Cylinder(__SCREW_D/2, __SCREW_HEAD_THICKNESS, align=(Align.CENTER,Align.CENTER,Align.MIN))

if __name__ == '__main__':
    from ocp_vscode import *
    show_all()