import csv
import sys
from copy import deepcopy
from build123d import *
from src.parts import *
from src.apiaster_case_config import *
from ocp_vscode import *


def get_svg_height(file):
    import xml.etree.ElementTree as ET
    tree = ET.parse(file)
    root = tree.getroot()
    return float(root.get("height", "0.0mm").removesuffix("mm"))


def convert_part_dict(part):
    return {k: (float(v) if k == 'PosX' or k == 'PosY' or k == 'Rot' else v) for k, v in part.items()}


def get_parts(filename):
    with open(filename, encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return dict([(x['Ref'], convert_part_dict(x)) for x in reader])


SVG_FILE_MAIN = "case/assets/apiaster-no-thumbs.svg"
SVG_FILE_THUMBS = "case/assets/apiaster-thumbs.svg"
POSITION_FILE = "case/assets/apiaster-all-pos.csv"
parts = get_parts(POSITION_FILE)
main_svg = import_svg(SVG_FILE_MAIN)
thumb_svg = import_svg(SVG_FILE_THUMBS)
main_edges = Wire.combine(main_svg.edges(), tol=0.05).wires()[
    0].clean().moved(Location((0, -get_svg_height(SVG_FILE_MAIN), 0))).order_edges()
thumb_wire = Wire.combine(thumb_svg.edges(), tol=0.05).wires()[
    0].clean().moved(Location((0, -get_svg_height(SVG_FILE_THUMBS), 0)))
thumb_origin = thumb_wire.order_edges()[-1].vertices()[1].to_tuple()

thumb_part_ids = []


def get_switches(args, left_side=True, tray=False, frame=False, keycaps=False):
    selected_thumbs = []
    selected_switches = base
    selected_switches += inner[args.inner_index]
    selected_switches += pinky_out[args.outer_keys]
    selected_switches += [pinky[x] for x in args.pinkies]
    if not args.remove_num_row:
        selected_switches += numbers[args.inner_index]
    for k in args.thumbs:
        selected_thumbs += thumbs[args.thumb_type][k]

    if tray:
        return [
            Pos(s['PosX'], s['PosY'], PCB_THICKNESS) * Rot(0, 0, s['Rot']) *
            switch_tray_cutout.tray_cutout(k, args)
            for k, s in parts.items() if k in selected_switches
        ] + [
            Pos(args.thumb_adjustment[0], -args.thumb_adjustment[1])*Pos(*thumb_origin)*Rot(
                0, 0, -args.thumb_adjustment[2])*Pos(*[-x for x in thumb_origin]) * Pos(s['PosX'], s['PosY'], PCB_THICKNESS) * Rot(0, 0, s['Rot']) *
            switch_tray_cutout.tray_cutout(k, args)
            for k, s in parts.items() if k in selected_thumbs
        ]
    if frame:
        hotswap = cpg135001s30.hotswap if args.switch == 'choc' else mx.hotswap
        return [
            Pos(s['PosX'], s['PosY']) * Rot(0, 0, s['Rot']) *
            (hotswap if left_side else mirror(
                hotswap, Plane.YZ))
            for k, s in parts.items() if k in selected_switches
        ] + [
            Pos(args.thumb_adjustment[0], -args.thumb_adjustment[1])*Pos(*thumb_origin)*Rot(
                0, 0, -args.thumb_adjustment[2])*Pos(*[-x for x in thumb_origin]) * Pos(s['PosX'], s['PosY']) * Rot(0, 0, s['Rot']) *
            (hotswap if left_side else mirror(
                hotswap, Plane.YZ))
            for k, s in parts.items() if k in selected_thumbs
        ]
    if keycaps:
        keycap = switch_tray_cutout.keycap
        return Compound([
            Pos(s['PosX'], s['PosY'], PCB_THICKNESS) * Rot(0, 0, s['Rot'])
            for k, s in parts.items() if k in selected_switches
        ] * (keycap if left_side else Rot(0, 180, 0) * mirror(keycap, Plane.XY)) + [
            Pos(args.thumb_adjustment[0], -args.thumb_adjustment[1])*Pos(*thumb_origin)*Rot(
                0, 0, -args.thumb_adjustment[2])*Pos(*[-x for x in thumb_origin]) * Pos(s['PosX'], s['PosY'], PCB_THICKNESS) * Rot(0, 0, s['Rot'])
            for k, s in parts.items() if k in selected_thumbs
        ] * (keycap if left_side else Rot(0, 180, 0) * mirror(keycap, Plane.XY)))
    switch = switch_tray_cutout.switch if args.switch == 'choc' else switch_tray_cutout.mx_switch
    return Compound([
        Pos(s['PosX'], s['PosY'],PCB_THICKNESS) * Rot(0, 0, s['Rot'])
        for k, s in parts.items() if k in selected_switches
    ] * (switch if left_side else Rot(0, 180, 0) * mirror(switch, Plane.XY)) + [
        Pos(args.thumb_adjustment[0], -args.thumb_adjustment[1])*Pos(*thumb_origin)*Rot(
            0, 0, -args.thumb_adjustment[2])*Pos(*[-x for x in thumb_origin]) * Pos(s['PosX'], s['PosY'], PCB_THICKNESS) * Rot(0, 0, s['Rot'])
        for k, s in parts.items() if k in selected_thumbs
    ] * (switch if left_side else Rot(0, 180, 0) * mirror(switch, Plane.XY)))


def make_frame(pcb_face, cut_face, args, left_side):
    thumb_objects = []

    bottom_thickness = BOTTOM_THICKNESS
    if args.smd_diodes:
        bottom_thickness += BOTTOM_THICKNESS_ADJUST[0]
    if args.tenting == 'magsafe':
        bottom_thickness += BOTTOM_THICKNESS_ADJUST[1]
    # Initial frame
    frame_face = \
        offset(pcb_face.faces(), amount=PCB_EDGE_GAP + SIDE_WALL_THICKNESS)
    frame = extrude(frame_face, amount=-bottom_thickness)
    if args.switch == 'choc':
        WALL_HEIGHT_ABOVE_PCB = CHOC_PCB_SWITCH_SNAPON_DIST if args.low_case else CHOC_SWITCH_HEIGHT_ABOVE_PCB
    else:
        WALL_HEIGHT_ABOVE_PCB = MX_PCB_SWITCH_SNAPON_DIST if args.low_case else MX_SWITCH_HEIGHT_ABOVE_PCB

    frame += extrude(frame_face, amount=PCB_THICKNESS+WALL_HEIGHT_ABOVE_PCB)
    frame = \
        chamfer(frame.edges().filter_by(Plane.XY),
                length=SIDE_WALL_THICKNESS/2)
    cutout_face = offset(pcb_face.face(), amount=PCB_EDGE_GAP)
    frame -= extrude(cutout_face, amount=PCB_THICKNESS+WALL_HEIGHT_ABOVE_PCB)
    frame -= extrude(cut_face, amount=-1.4)

    # Cutting out parts
    frame -= [
        Pos(v['PosX'], v['PosY']) * Rot(0, 0, v['Rot'])
        for v in parts.values()
        if v['Val'] == 'Jumper_2_Open'
    ] * jumpers.solder_gap
    frame -= get_switches(args, left_side=left_side, frame=True)
    frame -= Pos(parts['J5']['PosX'], parts['J5']['PosY']) * \
        Rot(0, 0, parts['J5']['Rot']) * \
        thumb_reattachment.cut_main
    if args.battery == 'coin':
        frame -= Pos(parts['BT1']['PosX'], parts['BT1']['PosY']) * \
            Rot(0, 0, parts['BT1']['Rot']) * \
            coin_cell_holder.solder_gap
    elif args.battery == 'lipo':
        frame -= Pos(parts['J2']['PosX'], parts['J2']['PosY']) * \
            Rot(0, 0, parts['J2']['Rot']) * jst.solder_gap
    if args.tenting == 'magsafe':
        magsafe_cut = tenting.magsafe + \
            extrude(tenting.magsafe.faces().filter_by(
                Plane.XY)[0], bottom_thickness * 2)
        frame -= Pos(parts['H1']['PosX'], parts['H1']['PosY'], -max(cpg135001s30.HOTSWAP_HEIGHT, diode.DIODE_HEIGHT)) * \
            Rot(0, 0, parts['H1']['Rot']) * magsafe_cut
    if args.tenting == 'puck':
        frame -= Pos(parts['H1']['PosX'], parts['H1']['PosY']) * \
            Rot(0, 0, parts['H1']['Rot']) * tenting.puck
    if args.mcu == 'xiao' or args.mcu == 'either':
        mcu_location = Pos(parts['U1']['PosX'], parts['U1']['PosY'])
        frame -= mcu_location * \
            Rot(0, 0, parts['U1']['Rot']) * xiao.xiao_solder_gap
        frame -= Pos(0, 3, PCB_THICKNESS + (args.mcu_socket_height if not args.smd_mcu else 0)) * mcu_location * \
            Rot(0, 0, parts['U1']['Rot']) * xiao.usb_c_cable_bot
    if args.mcu == 'rp2040-zero' or args.mcu == 'either':
        mcu_location = Pos(
            parts['U1']['PosX'], parts['U1']['PosY'])
        frame -= mcu_location * \
            Rot(0, 0, parts['U1']['Rot']) * rpi.rp_solder_gap
        if left_side:
            frame -= Pos(0, 0, PCB_THICKNESS + (args.mcu_socket_height if not args.smd_mcu else 0)) * mcu_location * \
            Rot(0, 0, parts['U1']['Rot']) * xiao.usb_c_cable_bot
    if not args.block_usb:
        frame -=  Pos(parts['J1']['PosX'], parts['J1']['PosY']) * \
            Rot(0, 0, 180+parts['J1']['Rot']) * usb_socket.solder_gap
    if not args.no_usb_a and not args.block_usb:
        cable =  Pos(parts['J1']['PosX'], parts['J1']['PosY'], PCB_THICKNESS)  *  \
            Rot(0, 0, 180+parts['J1']['Rot']) * usb_socket.usb_a_cable
        frame -= cable
        frame -= cable

    if not args.smd_diodes:
        frame -= [Pos(v['PosX'], v['PosY']) * Rot(0, 0, v['Rot']) for v in parts.values()
                  if v['Val'] == '1N4148'] * diode.sod27_diode_combo
    else:
        frame -= [Pos(v['PosX'], v['PosY']) * Rot(0, 0, v['Rot']) for v in parts.values()
                  if v['Val'] == '1N4148'] * diode.sod123_diode_combo

    # Cutting out feet and screws
    frame -= Plane.XY * [
        Pos(x['PosX'], x['PosY'], -bottom_thickness+.5)
        for x in parts.values()
        if x['Val'] == 'MountingHole' and x['Ref'] not in ['H6', 'H7']
    ] * mirror(CounterSinkHole(radius=1.25, counter_sink_radius=2.2, depth=bottom_thickness*2), Plane.XY)
    frame -= Plane.XY * [
        Pos(args.thumb_adjustment[0], -args.thumb_adjustment[1])*Pos(*thumb_origin)*Rot(
            0, 0, -args.thumb_adjustment[2])*Pos(*[-x for x in thumb_origin]) *
        Pos(x['PosX'], x['PosY'], -bottom_thickness+.5)
        for x in parts.values()
        if x['Ref'] in ['H6', 'H7']
    ] * mirror(CounterSinkHole(radius=1.25, counter_sink_radius=2.2, depth=bottom_thickness*2), Plane.XY)
    for p in RUBBER_FEET_POSITIONS[:-1]:
        frame -= Pos(p[0], -p[1], -bottom_thickness) * Cylinder(RUBBER_FEET_DIAMETER/2 + RUBBER_FEET_DIAMETER_TOL,
                                                                RUBBER_FEET_CUTOUT_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MIN))
    frame -= Pos(args.thumb_adjustment[0], -args.thumb_adjustment[1])*Pos(*thumb_origin)*Rot(
        0, 0, -args.thumb_adjustment[2])*Pos(*[-x for x in thumb_origin]) * Pos(RUBBER_FEET_POSITIONS[-1][0], -RUBBER_FEET_POSITIONS[-1][1], -bottom_thickness) * Cylinder(4,
                                                                                                                                                                           0.8, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return frame


def make_tray(pcb_face, args, left_side=True):
    if args.switch == 'choc':
        WALL_HEIGHT_ABOVE_PCB = CHOC_PCB_SWITCH_SNAPON_DIST if args.low_case else CHOC_SWITCH_HEIGHT_ABOVE_PCB
    else:
        WALL_HEIGHT_ABOVE_PCB = MX_PCB_SWITCH_SNAPON_DIST if args.low_case else MX_SWITCH_HEIGHT_ABOVE_PCB
    tray = Pos(0, 0, PCB_THICKNESS) * \
        extrude(pcb_face, amount=WALL_HEIGHT_ABOVE_PCB)
    if not args.block_usb:
        tray -= Pos(parts['J1']['PosX'], parts['J1']['PosY'], PCB_THICKNESS) * Rot(
            0, 0, 180+parts['J1']['Rot']) * usb_socket.usb_a_cutout
        if not 'usb' in args.expose:
            tray += Pos(parts['J1']['PosX'], parts['J1']['PosY'], PCB_THICKNESS) * Rot(
                0, 0, 180+parts['J1']['Rot']) * usb_socket.usb_a_shell
    if not args.block_usb and not args.no_usb_a:
        tray -= Pos(parts['J1']['PosX'], parts['J1']['PosY'], PCB_THICKNESS) * Rot(
            0, 0, 180+parts['J1']['Rot']) * usb_socket.usb_a_cable

    tray -= [
        Pos(x['PosX'], x['PosY'], PCB_THICKNESS)
        for x in parts.values()
        if x['Val'] == 'MountingHole' and x['Ref'] not in ['H6', 'H7']
    ] * nut.nut_cut
    tray -= [Pos(args.thumb_adjustment[0], -args.thumb_adjustment[1])*Pos(*thumb_origin)*Rot(
        0, 0, -args.thumb_adjustment[2])*Pos(*[-x for x in thumb_origin]) *
        Pos(x['PosX'], x['PosY'], PCB_THICKNESS)
        for x in parts.values()
        if x['Ref'] in ['H6', 'H7']
    ] * nut.nut_cut
    tray -= Pos(parts['J5']['PosX'], parts['J5']['PosY'],PCB_THICKNESS) * \
        Rot(0, 0, parts['J5']['Rot']) * \
        thumb_reattachment.cut_top
    tray -= Pos(args.thumb_adjustment[0], -args.thumb_adjustment[1])*Pos(parts['J4']['PosX'], parts['J4']['PosY'],PCB_THICKNESS) * \
        Rot(0, 0, parts['J4']['Rot'])*Rot(
        0, 0, -args.thumb_adjustment[2]) * \
        thumb_reattachment.cut_top

    if args.tenting == 'puck':
        tray -= Pos(parts['H1']['PosX'], parts['H1']['PosY'], PCB_THICKNESS) * \
            Rot(0, 0, parts['H1']['Rot']) * tenting.puck

    if not args.smd_diodes:
        tray -= [Pos(v['PosX'], v['PosY'], PCB_THICKNESS) * Rot(0, 0, v['Rot']) for v in parts.values()
                  if v['Val'] == '1N4148'] * diode.sod27_diode_combo

    if args.battery == 'coin':
        tray -= Pos(parts['J3']['PosX'], parts['J3']['PosY'],
                    PCB_THICKNESS) * Rot(0, 0, parts['J3']['Rot']) * Box(31, 6, 3, align=(Align.CENTER, Align.CENTER, Align.MIN))
        tray -= Pos(parts['BT1']['PosX'], parts['BT1']['PosY'],
                    PCB_THICKNESS) * Rot(0, 0, parts['BT1']['Rot']) * coin_cell_holder.housing_cut
        if not 'battery' in args.expose:
            tray += Pos(parts['BT1']['PosX'], parts['BT1']['PosY'],
                        PCB_THICKNESS) * Rot(0, 0, parts['BT1']['Rot']) * coin_cell_holder.shell
    elif args.battery == 'lipo':
        tray -= Pos(parts['J2']['PosX'], parts['J2']['PosY'], PCB_THICKNESS) * \
            Rot(0, 0, parts['J2']['Rot']) * jst.box
        tray -= Pos(parts['BT1']['PosX'], parts['BT1']['PosY'],
                    PCB_THICKNESS) * Rot(0, 0, parts['BT1']['Rot']) * jst.hollow
        if 'battery' in args.expose:
            tray -= Pos(parts['J2']['PosX'], parts['J2']['PosY'], PCB_THICKNESS) * \
                Rot(0, 0, parts['J2']['Rot']) * extrude(
                    jst.box.faces().filter_by(Plane.XY)[-1], WALL_HEIGHT_ABOVE_PCB)
            tray -= Pos(parts['BT1']['PosX'], parts['BT1']['PosY'],
                        PCB_THICKNESS) * Rot(0, 0, parts['BT1']['Rot']) * extrude(jst.hollow.faces().filter_by(Plane.XY)[-1], WALL_HEIGHT_ABOVE_PCB)
    
    if args.mcu == 'xiao':
        mcu_location = Pos(parts['U1']['PosX'], parts['U1']['PosY'])
        tray -= Pos(0, 0, PCB_THICKNESS + (args.mcu_socket_height if not args.smd_mcu else 0)) * mcu_location * \
            Rot(0, 0, parts['U1']['Rot']) * (xiao.xiao_box_cut + xiao.xiao_skylights)    
        box = Pos(0, 0, PCB_THICKNESS + (args.mcu_socket_height if not args.smd_mcu else 0)) * mcu_location * \
            Rot(0, 0, parts['U1']['Rot']) * (xiao.xiao_box if left_side else mirror(xiao.xiao_box, Plane.YZ))
        split_box = split(box, Plane(tray.faces().filter_by(
            Plane.XY).sort_by(Axis.Z)[0]), keep=Keep.BOTTOM)
        split_box -= Pos(0, 3, PCB_THICKNESS + (args.mcu_socket_height if not args.smd_mcu else 0)) * mcu_location * \
            Rot(0, 0, parts['U1']['Rot']) * xiao.usb_c_cable_top
        tray -= Pos(0, 3, PCB_THICKNESS + (args.mcu_socket_height if not args.smd_mcu else 0)) * mcu_location * \
            Rot(0, 0, parts['U1']['Rot']) * xiao.usb_c_cable_top
    elif args.mcu == 'rp2040-zero':
        if left_side:
            mcu_location = Pos(
                parts['U1']['PosX'], parts['U1']['PosY'])
            tray -= Pos(0, 0, PCB_THICKNESS + (args.mcu_socket_height if not args.smd_mcu else 0)) * mcu_location * \
            Rot(0, 0, parts['U1']['Rot']) * (rpi.rp_box_cut + rpi.rp_skylights)    
            box = Pos(0, 0, PCB_THICKNESS + (args.mcu_socket_height if not args.smd_mcu else 0)) * mcu_location * \
                Rot(0, 0, parts['U1']['Rot']) * rpi.rp_box
            split_box = split(box, Plane(tray.faces().filter_by(
                Plane.XY).sort_by(Axis.Z)[0]), keep=Keep.BOTTOM)
            split_box -= Pos(0, 3, PCB_THICKNESS + (args.mcu_socket_height if not args.smd_mcu else 0)) * mcu_location * \
                Rot(0, 0, parts['U1']['Rot']) * xiao.usb_c_cable_top
            tray -= Pos(0, 0, PCB_THICKNESS + (args.mcu_socket_height if not args.smd_mcu else 0)) * mcu_location * \
                Rot(0, 0, parts['U1']['Rot']) * xiao.usb_c_cable_top
        elif not args.smd_mcu:
            mcu_location = Pos(
                parts['U1']['PosX'], parts['U1']['PosY']-.6, PCB_THICKNESS)
            socket_box = Box(17.78, 20.95, args.mcu_socket_height, align=(Align.CENTER, Align.MAX, Align.MIN))
            tray -= mcu_location * \
                Rot(0, 0, parts['U1']['Rot']) * split(offset(socket_box, 0.5), Plane.XY)
            socket_box = offset(socket_box, 1.5) - offset(socket_box, 0.5)
            tray += mcu_location * \
                Rot(0, 0, parts['U1']['Rot']) * split(socket_box, Plane.XY)
    else:
        mcu_location = Pos(
            parts['U1']['PosX'], parts['U1']['PosY'])
        tray -= mcu_location * \
            Rot(0, 0, parts['U1']['Rot']) * rpi.rp_solder_gap
        tray -= Pos(0, 0, PCB_THICKNESS + (args.mcu_socket_height if not args.smd_mcu else 0)) * mcu_location * \
            Rot(0, 0, parts['U1']['Rot']) * xiao.usb_c_cable_top
    tray -= get_switches(args, left_side=left_side, tray=True)
    tray -= [
        Pos(v['PosX'], v['PosY'],PCB_THICKNESS) * Rot(0, 0, v['Rot'])
        for v in parts.values()
        if v['Val'] == 'Jumper_2_Open'
    ] * jumpers.solder_gap
    # For some reason it runs forever if split_box is added to tray
    if args.mcu != 'either' and 'mcu' not in args.expose and not (args.mcu == 'rp2040-zero' and not left_side):
        split_box -= get_switches(args, left_side=left_side, tray=True)
        split_box -= [
        Pos(v['PosX'], v['PosY'],PCB_THICKNESS) * Rot(0, 0, v['Rot'])
        for v in parts.values()
        if v['Val'] == 'Jumper_2_Open'
    ] * jumpers.solder_gap
        return Compound([tray, split_box])
    else:
        return tray


def make_case(args, left_side=True):
    thumb_edges = (Pos(args.thumb_adjustment[0], -args.thumb_adjustment[1])*Pos(*thumb_origin)*Rot(
        0, 0, -args.thumb_adjustment[2])*Pos(*[-x for x in thumb_origin]) * thumb_wire).order_edges()
    if args.thumb_adjustment != (0,0,0):
        thumb_edges = thumb_edges[1:]
    edge_verts = (
        thumb_edges[-1].vertices()[1], main_edges[0].vertices()[0], thumb_edges[0].vertices()[
            0], main_edges[-1].vertices()[1], thumb_edges[-2].vertices()[0]
    )
    close1 = [
        Edge.make_line(edge_verts[0], edge_verts[1])
    ] if edge_verts[0].to_tuple() != edge_verts[1].to_tuple() else []
    close2 = [
        Edge.make_line(edge_verts[2], edge_verts[3])
    ] if edge_verts[2].to_tuple() != edge_verts[3].to_tuple() else []
    mid_point = Vertex([x/2 for x in edge_verts[3]+edge_verts[1]])
    close3 = [
        Edge.make_line(edge_verts[4], mid_point)
    ]
    close4 = [
        Edge.make_line(mid_point, edge_verts[3])
    ]
    pcb_face = make_face([main_edges, thumb_edges] + close1 + close2)
    cut_face = offset(make_face([thumb_edges[:-2]] + close2+close3+close4), -4)
    tray = make_tray(pcb_face, args, left_side)
    frame = make_frame(pcb_face, cut_face, args, left_side)
    if not left_side:
        tray = Rot(0, 180, 0) * mirror(tray, Plane.XY)
        frame = Rot(0, 180, 0) * mirror(frame, Plane.XY)
    return tray, frame


def get_mcu(args, left_side=True):
    mcu_location = Pos(0, 0, PCB_THICKNESS + (args.mcu_socket_height if not args.smd_mcu else 0)) * \
            Rot(0, 0, parts['U1']['Rot']) * Pos(parts['U1']['PosX'], parts['U1']['PosY'])
    if args.mcu == 'xiao':
        xiao = mcu_location * Pos(6.11, -12.28, 0.25) * Rot(90, 90, 0) * \
            import_step('case/assets/XIAO-nRF52840 v15.step')
        if not left_side:
            xiao = Rot(0, 180, 0) * mirror(xiao, Plane.XY)
        return xiao
    if args.mcu == 'rp2040-zero':
        rp2040_zero = mcu_location * Pos(0, -13.08, -0.12 + 0.25) * Rot(90,
                                                                        0, 0) * import_step('case/assets/RP2040-ZERO.STEP')
        if not left_side:
            rp2040_zero = Rot(0, 180, 0) * Box(0.1,0.1,0.1)
        return rp2040_zero
    xiao = mcu_location * Pos(6.11, -12.28, 0.25) * Rot(90, 90, 0) * \
        import_step('case/assets/XIAO-nRF52840 v15.step')
    xiao += mcu_location * Pos(0, -13.08, -0.12 + 0.25) * Rot(90,
                                                              0, 0) * import_step('case/assets/RP2040-ZERO.STEP')
    if not left_side:
        xiao = Rot(0, 180, 0) * mirror(xiao, Plane.XY)
    return xiao