from build123d import *
from copy import deepcopy

__SOLDER_TOL = 1.4*MM
__CYL_TOL = 2.4*MM

al=(Align.CENTER, Align.CENTER, Align.MAX)

solder_gap = Pos(0, 2.5) * Box(10*MM, 3*MM, __SOLDER_TOL, align=al) \
    + Pos(-6.57, 5.22) * Cylinder(1.5*MM, __CYL_TOL, align=al) \
    + Pos(6.57, 5.22) * Cylinder(1.5*MM, __CYL_TOL, align=al)

usb_a_cutout = Box(15*MM, 17.2*MM, 8*MM,
                   align=(Align.CENTER, Align.MIN, Align.MIN)) \
                + Pos(0,16.2) *Box(16*MM, 1*MM, 9*MM,
                   align=(Align.CENTER, Align.MIN, Align.MIN))
usb_a_shell = offset(usb_a_cutout, 1.2*MM, kind=Kind.INTERSECTION)
usb_a_shell -= Box(40, 40, 40, align=(Align.CENTER, Align.CENTER, Align.MAX))
usb_a_shell -= Pos(0, 20) * Box(40, 40, 40,
                                align=(Align.CENTER, Align.MIN, Align.CENTER))
usb_a_shell += extrude(usb_a_shell.faces().filter_by(Plane.XZ)[-1],0.2)
usb_a_cable = Pos(0,0,7*MM) * Box(12.4*MM, 17.2+3.6*MM, 5.12*MM,
                   align=(Align.CENTER, Align.MIN, Align.MAX))
top_plane = Plane(usb_a_cable.faces().filter_by(Plane.XZ).sort_by(-Axis.Y)[0])
chamfer_box = top_plane * Box( 5.12+1.2*MM,12.4+1.2*MM, 2.8*MM,
                   align=(Align.CENTER, Align.CENTER, Align.MAX))
chamfer_box = chamfer(chamfer_box.edges().group_by(Axis.Y)[0], length=0.6)
usb_a_cable += chamfer_box
usb_a_cable_cut = top_plane *Pos(0,0,-2) *  Box(10*MM, 18*MM, 20*MM,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
usb_a_cable_cut = fillet(usb_a_cable_cut.edges().group_by(Axis.Y)[1:], radius=1)
usb_a_cable_cut = split(usb_a_cable_cut, Plane.XY.offset(2), keep=Keep.BOTTOM)
usb_a_cable_cut += extrude(usb_a_cable_cut.faces().sort_by(Axis.Z)[-1], 20)
usb_a_cable += usb_a_cable_cut
usb_a_shell_a = split(usb_a_shell,Plane(usb_a_shell.faces().filter_by(Plane.XZ).sort_by(Axis.Y)[1]))
usb_a_shell_b = Pos(0,15) *Box(18.4*MM, 3.6*MM, 10.2*MM,
                   align=(Align.CENTER, Align.MIN, Align.MIN))\
                    +Pos(0,16) * Rot(0,0,180) * extrude(Triangle(a=14,b=30,c=30, align=(Align.CENTER, Align.MIN)),10.2)
usb_a_shell_b = fillet(usb_a_shell_b.edges().sort_by(Axis.Y)[1:].group_by(Axis.Z)[1:],1)
usb_a_shell_b = split(usb_a_shell_b, Plane(usb_a_shell_a.faces().filter_by(Plane.XZ).sort_by(Axis.Y)[0]), keep=Keep.BOTTOM)
usb_a_shell_a += extrude(usb_a_shell_a.faces().filter_by(Plane.XZ).sort_by(Axis.Y)[-1], until=Until.LAST, target=usb_a_shell_b)
usb_a_shell_a = fillet(usb_a_shell_a.edges().filter_by(Axis.Z).sort_by(Axis.Y)[:2], 1)
usb_a_shell = usb_a_shell_a+usb_a_shell_b
usb_a_shell -= usb_a_cutout

if __name__ == '__main__':
    from ocp_vscode import *
    show_all()
