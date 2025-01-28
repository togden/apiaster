from build123d import *

__solder_tol = 1.4*MM

rp2040_zero = Pos(0,-13.08,-0.12 + 0.25) *Rot(90, 0, 0) * import_step('case/assets/RP2040-ZERO.STEP')

rp_solder_gap = Pos(0, -1.12*MM,) * \
    Box(18*MM, 25*MM, __solder_tol, align=(Align.CENTER, Align.MAX, Align.MAX))
rp_solder_gap += Box(18.6, 25.6, 20,
                     align=(Align.CENTER, Align.MAX, Align.MIN))

rp_box = Pos(0,-1.33) * Box(18, 23.5, 4.5, align=(Align.CENTER, Align.MAX, Align.MIN))
rp_box_big = rp_box + extrude(rp_box.faces().filter_by(Plane.XY)[-1], 20)

rp_box = Pos(0,-1.33) * Box(18, 23.5, 1.2, align=(Align.CENTER, Align.MAX, Align.MIN))
shield_box = Pos(0,-1.33, 1.2)*Box(12.6, 23.5,1.85, align=(Align.CENTER, Align.MAX, Align.MIN))
shield_box_short = Pos(0,-1.33, 1.2)*Box(12.6, 20,1.85, align=(Align.CENTER, Align.MAX, Align.MIN))
box_e = Pos(0,.9,-2) * Box(11.96+4.41*2 + .22, 8.77+1,1.5+4.46+2, align=(Align.CENTER, Align.MAX, Align.MIN))
box_e = fillet(box_e.edges().filter_by(Axis.Y).group_by(Axis.Z)[-1], 1.41)
box_e_cut =Pos(0,.9) * Box(8.96, 8.27,4.46, align=(Align.CENTER, Align.MAX, Align.MIN)) 
box_e_cut = fillet(box_e_cut.edges().filter_by(Axis.Y).group_by(Axis.Z)[-1], 1.25)
rp_box_cut = offset(rp_box+shield_box_short + box_e_cut, 0.5)
rp_box_cut = split(rp_box_cut, Plane.XY)
rp_box_cut+= extrude(rp_box_cut.faces().sort_by(Axis.Z)[0], 20)
rp_box = offset(rp_box, 1.5, kind=Kind.INTERSECTION) 
shield_box = offset(shield_box, 1.5, kind=Kind.INTERSECTION) 
shield_box = fillet(shield_box.edges().group_by(Axis.Z)[-1].filter_by(Axis.Y),1.05)
rp_box += box_e
rp_box = fillet( rp_box.edges().filter_by(Plane.XZ).filter_by(Axis.Z).sort_by(Axis.Z)[2:6],1)
rp_box = fillet(rp_box.edges().group_by(Axis.Z)[1],1)
rp_box = fillet(rp_box.edges().group_by(Axis.Z)[-1].sort_by(Axis.Y)[0],1)
rp_box += shield_box
rp_box -= rp_box_cut
rp_box = split(rp_box, Plane.XY)
rp_box += extrude(rp_box.faces().filter_by(Plane.XY).sort_by(Axis.Z)[0], 20)
rp_skylights =  offset(Pos(4.64, -17.45) *Rot(0,0,90) * extrude(SlotCenterToCenter(0.8, 2.2), 30) + Pos(-4.64, -17.45) *  Rot(0,0,90) * extrude(SlotCenterToCenter(0.8, 2.2), 30),0.3)
rp_box -= rp_skylights

if __name__ == '__main__':
    from ocp_vscode import *
    show_all()