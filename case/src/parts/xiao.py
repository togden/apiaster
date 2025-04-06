from build123d import *

__solder_tol = 1.4*MM

xiao = Pos(6.11, -12.28, 0.25) * Rot(90, 90, 0) * \
     import_step('case/assets/XIAO-nRF52840 v15.step')

xiao_solder_gap = Pos(0, -1.12*MM,) * \
    Box(18*MM, 20*MM, __solder_tol, align=(Align.CENTER, Align.MAX, Align.MAX))

usb_c_cable = Pos(0, 1.15, 1.6+3.42/2 - .7 + 0.25) * \
    Box(13, 20, 7, align=(Align.CENTER, Align.MIN, Align.CENTER))
usb_c_cable = fillet(usb_c_cable.edges().filter_by(Axis.Y), 2)
usb_c_port = Plane(usb_c_cable.faces().filter_by(Plane.XZ)[
                   0]) * Box(3.21, 8.94, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
usb_c_port = fillet(usb_c_port.edges().filter_by(Axis.Y), 1.25)

usb_c_cable_top, usb_c_cable_bot = split(usb_c_cable, Plane.XY.move(
    Location((0, 1.15, 1.6+3.42/2 - .7 + 0.25))), keep=Keep.BOTH)
usb_c_port_top, usb_c_port_bot = split(usb_c_port, Plane.XY.move(
    Location((0, 1.15, 1.6+3.42/2 - .7 + 0.25))), keep=Keep.BOTH)
usb_c_cable_bot += usb_c_port_bot
usb_c_cable_top += extrude(usb_c_cable_top.faces().filter_by(Plane.XY)[0], 10)
usb_c_cable_bot += extrude(usb_c_cable_bot.faces().filter_by(Plane.XY)[0], 10)
usb_c_port_top += extrude(usb_c_port_top.faces().filter_by(Plane.XY)[0], 10)
usb_c_port_top = offset(usb_c_port_top, 0.5)
usb_c_cable_top += usb_c_port_top
led_skylight = Pos(5.7, -2.9, 1.55+4.41) * CounterSinkHole(radius=1.05, counter_sink_radius=1.2, depth=20) + Pos(5.6, -.63, 1.55) * extrude(SlotCenterToCenter(0.5, .8), 10)\
    + Pos(4.8, -3+.23/2, 2) * Box(4, 7-.23, 3-0.04, align=(Align.CENTER,Align.CENTER,Align.MIN))
xiao_skylights = led_skylight+\
    Pos(-6, -2, 2) * Rot(0,0,90) * extrude(SlotCenterToCenter(1,2.3), 10)+\
        Pos(-5.4, -3+.23/2, 2) * extrude(Rectangle(4.4,7-.23), 3-0.04)

xiao_box =extrude(Rectangle(17.78, 20.95,align=(Align.CENTER, Align.MAX, Align.MIN)), 2.19) 
shield_box = Pos(0,-17.53-3.42, 1.6)*Box(12.6, 10.6+6.93+3.42,2.8-1.15 , align=(Align.CENTER, Align.MIN, Align.MIN))
box_e = Pos(0,1.5)* Box(11.96+4.41*2, 8.77,1.5+4.46, align=(Align.CENTER, Align.MAX, Align.MIN))
box_e = fillet(box_e.edges().filter_by(Axis.Y).group_by(Axis.Z)[-1], 2)
box_e_cut = Pos(0,1.5)* Box(8.96, 8.27-1,4.46, align=(Align.CENTER, Align.MAX, Align.MIN)) 
box_e_cut = fillet(box_e_cut.edges().filter_by(Axis.Y).group_by(Axis.Z)[-1], 1.25)
xiao_box_big = xiao_box + extrude(xiao_box.faces().filter_by(Axis.Z)[-1], 10)
xiao_box_cut = offset(xiao_box+shield_box + box_e_cut, 0.5, kind=Kind.INTERSECTION)
xiao_box_cut += extrude(xiao_box_cut.faces().sort_by(Axis.Z)[0], 20)
xiao_box_ev = xiao_box+shield_box+box_e_cut
xiao_box = offset(xiao_box, 1.5, kind=Kind.INTERSECTION) 
shield_box = offset(shield_box, 1.5, kind=Kind.INTERSECTION)
shield_box -= Pos(0,1.5) * Box(40,0.6, 40, align=(Align.CENTER, Align.MAX, Align.CENTER))
shield_box = fillet(shield_box.edges().group_by(Axis.Z)[-1].filter_by(Axis.Y),1.05)
xiao_box += box_e
xiao_box -= Pos(0,1.5) * Box(40,0.6, 40, align=(Align.CENTER, Align.MAX, Align.CENTER))
xiao_box = fillet(xiao_box.edges().group_by(Axis.Z)[1],1.98)
xiao_box = fillet( xiao_box.edges().group_by(Axis.Z)[2].sort_by(Axis.Y)[0], 1)
xiao_box = fillet(xiao_box.edges().group_by(Axis.Z)[-1].sort_by(Axis.Y)[0],1)
xiao_box += shield_box
xiao_box -= xiao_box_cut
xiao_box = split(xiao_box, Plane.XY)
xiao_box += extrude(xiao_box.faces().filter_by(Plane.XY).sort_by(Axis.Z)[0], 20)
xiao_box -= xiao_skylights


xiao_skylight_button = Pos(-6, -2, 2) * Rot(0,0,90) * extrude(SlotCenterToCenter(1, 1.6), 4.7)+\
        Pos(-6, -2.9, 2) * chamfer(extrude(Rectangle(2.6, 6), 2.8).edges().group_by(Axis.Z)[0], 1, 0.5)

xiao_button_stl = export_stl(xiao_skylight_button, "case/stl/apiaster-xiao-button.stl")
print(f"Export success case/stl/apiaster-xiao-button.stl: {xiao_button_stl}")

if __name__ == '__main__':
    from ocp_vscode import *
    show_all()
#Pos(0,-1.18) *
