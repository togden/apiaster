from build123d import *

__SNAPON_THICKNESS = 1.5*MM
__PCB_DIST_TO_SNAPON_STOPPER = 2.2*MM
__SWITCH_DIMS_INNER = 14*MM
__SWITCH_DIMS_OUTER = 15.6*MM
__SWITCH_RECT_ROUNDING = 0.4*MM
__PULLER_CUTOUT_DIMS = (3.8*MM, 2.3+0.45/2*MM, 1.2*MM)

switch = Pos(0, 0, 2.6) * Rot(90, -90, 0) * \
    import_step('case/assets/Kailh_PG1353.STEP')

mx_switch = Pos(-0.31, -0.31, 5.16) * Rot(180,0,-90) * \
    import_step('case/assets/asm_mx_asm_PCB.step')

keycap = Pos(0, 0, 2.6+3.7) * Rot(0, 0, 0) * \
    import_step('case/assets/ols-v1-r3.step')

keycaps = [
    Box(19.1*MM, 19.1*MM, 10*MM,
        align=(Align.CENTER, Align.CENTER, Align.MIN)),
    Box(19.1*MM, 1.5*19.1*MM, 10*MM,
        align=(Align.CENTER, Align.CENTER, Align.MIN)),
    # tucky thumb
    Box(18*MM, 17*MM, 10*MM,
        align=(Align.CENTER, Align.CENTER, Align.MIN)),
    # reachy thumb
    Pos(0.073, 0.16) * Box(18*MM, 28.901*MM, 10*MM,
                           align=(Align.CENTER, Align.CENTER, Align.MIN)),
    # middle thumb
    Rot(0, 0, 10) *
    extrude(make_face([
        Line((13.95, 12.5), (-10, 12.5)),
        Line((-10, -4.5), (-10, 12.5)),
        Line((13.95, 12.5), (5.98, -15.28)),
        Spline((5.98, -15.28), (-10, -4.5),
               tangents=[(-1, .35), (0, 1)], tangent_scalars=[2.37/100, 2.565/2.5])
    ]), 10),
]


def tray_cutout(switch_ref, args):
    tray_cutout = Pos(0, 0, __PCB_DIST_TO_SNAPON_STOPPER-__SNAPON_THICKNESS) *\
        extrude(RectangleRounded(__SWITCH_DIMS_INNER,  __SWITCH_DIMS_INNER,
                __SWITCH_RECT_ROUNDING), 20)
    tray_cutout += extrude(tray_cutout.faces().sort_by(Axis.Z)[0], 5)
    if args.switch == 'choc':
        tray_cutout += Box(__SWITCH_DIMS_OUTER, __SWITCH_DIMS_INNER, __PCB_DIST_TO_SNAPON_STOPPER -
                    __SNAPON_THICKNESS, align=(Align.CENTER, Align.CENTER, Align.MIN))  
    else: 
        tray_cutout += Box(__SWITCH_DIMS_INNER, __SWITCH_DIMS_OUTER,
                __SNAPON_THICKNESS+2, align=(Align.CENTER, Align.CENTER, Align.MIN))       
    tray_cutout += Pos(0, 0, __PCB_DIST_TO_SNAPON_STOPPER + (0 if args.switch == 'choc' else 2.8)) * Box(
        __PULLER_CUTOUT_DIMS[0], __PULLER_CUTOUT_DIMS[1]*2 + __SWITCH_DIMS_INNER, __PULLER_CUTOUT_DIMS[2], align=(Align.CENTER, Align.CENTER, Align.MAX))

    top_dist = __PCB_DIST_TO_SNAPON_STOPPER + (0 if args.switch == 'choc' else 2.8)
    if switch_ref == "RCa5-2|5-7":
        tray_cutout += Pos(0, 0, top_dist) * keycaps[4]
    elif switch_ref == "RCa5-3|5-8":
        tray_cutout += Pos(0, 0, top_dist) * keycaps[3]
    elif switch_ref == "RC5-3|5-8" and args.thumb_type in ['classic', 'flex']:
        tray_cutout += Pos(0, 0, top_dist) * keycaps[1]
    elif switch_ref == "RC5-4|5-9" and args.thumb_type == 'ripple':
        tray_cutout += Pos(0, 0, top_dist) * keycaps[2]
    elif switch_ref == "RC5-0|0-5" and args.outer_keys in ['upper-1.5u', 'all']:
        tray_cutout += Pos(0, 0, top_dist) * keycaps[1]
    else:
        tray_cutout += Pos(0, 0, top_dist) * keycaps[0]
    return tray_cutout


if __name__ == '__main__':
    from ocp_vscode import *
    show_all()
