import argparse
import sys


def tuple_of_ints(arg):
    return tuple(map(int, arg.split(',')))


parser = argparse.ArgumentParser(prog='make_case.py')
base = parser.add_argument_group('Base Settings')
component = parser.add_argument_group('Component Settings')
keys = parser.add_argument_group('Key Settings')
export = parser.add_argument_group('Export Settings')
display = parser.add_argument_group('Rendering Settings')
base.add_argument('--side', choices=['left', 'right'],
                  help="Which sides of the keyboard to build the case for. Note that your halves may differ e.g. in the choice of MCU. Defaults to both.")
base.add_argument('--export-stl', action="store_true",
                  help="Save case to file")
base.add_argument('--no-show', action="store_true",
                  help="Render case using ocp_vscode")
component.add_argument('--switch', choices=['mx', 'choc'], default='choc',
                       help="What type of switches are used")
component.add_argument('--mcu', choices=['xiao', 'rp2040-zero', 'either'], default='either',
                       help="MCU used. Will error if rp2040-zero is tried to be put on the RHS. 'either' will expose the MCU, similar to '--expose'. If you wish to be flexible between the two *and* cover the MCU, it is recommended that you print the frame with 'either', and print the tray with the MCU you're currently using. Default: 'either'")
component.add_argument('--smd-mcu', action="store_true",
                       help="Set this flag if MCU is mounted SMD")
component.add_argument('--mcu-socket-height', default=4.7, type=float,
                       help="The height of the sockets in millimeters above the PCB. Default 4.7mm (round pin sockets)")
component.add_argument('--battery', choices=['none', 'coin', 'lipo'], default='none',
                       help="Will error if 'xiao' or 'either' is selected as mcu and this is 'none'. Default: 'none'")
component.add_argument('--no-usb-a', action="store_true",
                       help="Set this flag if you're using a xiao and there will be no usb-A 3.0 port.")
component.add_argument('--block-usb', action="store_true",
                       help="Set this flag if you're using a xiao and there is a soldered usb-A 3.0 port that you wish to cover up.")
component.add_argument('--tenting', choices=['none', 'magsafe', 'puck'], default='none',
                       help="Integrated tenting options. A magsafe sticker (inner diameter 46mm, outer diameter 56mm, thickness 0.7mm or less) or the SplitKB tenting puck. Default: 'none'")
component.add_argument('--smd-diodes',
                       action="store_true", help="Set this flag if you are using SMD diodes. Will slightly reduce the height of the case.")
keys.add_argument('--outer-keys',
                  choices=['all', 'upper-1.5u', 'upper-1u', 'lower', 'none'], default='all', help="Which outer pinky keys should be enabled. All sets the upper key to 1.5u. Default: 'all'")
keys.add_argument('--inner-index', choices=['all', 'reduced', 'flex'], default='flex',
                  help="Adjust the number and position of the inner index keys for better comfort. Flex allows either configuration to be used.")
keys.add_argument('--remove-num-row', action="store_true",
                  help="Removes the num row keys by covering them up with the tray.")
keys.add_argument('--thumb-type', choices=['ripple', 'all-1u', 'classic', 'flex'], default='flex',
                  help="Select what thumb cluster type should be used. Classic is 1u-1u-1.5u. Flex allows for any of the three options, but may be less stable.")
keys.add_argument('--thumbs', action="extend", nargs="*", choices=['reachy', 'tucky', 'middle'], default=[
], help="Select which thumbs to use. Default all.")
keys.add_argument('--thumb-adjustment',  type=tuple_of_ints,
                  default=(0, 0, 0), help="Move the thumb cluster. --thumb-adjustment x,y,r where x is the number of mm that the cluster should be moved inwards, y is the number of mm that the cluster should be moved downwards, and r is the clockwise rotation in degrees around the outermost down-most corner of the cluster.")
keys.add_argument('--pinkies', action="extend", nargs="*", choices=['upper', 'home', 'lower'], default=[
], help="Select which pinky keys to use. Default all.")
component.add_argument('--expose', action="extend", nargs="*",
                       choices=['mcu', 'battery', 'usb'], default=[], help="Select components which shouldn't be covered up by the tray. Note that 'battery' only has an effect if 'coin' is selected,")
base.add_argument('--low-case', action="store_true",
                  help="If enabled, this will lower the height of the tray and frame such that they stop at the switch snap-on point. (You may need to expose some components)")
display.add_argument('--show-more', action="store_true",
                     help="Display the MCU, switches, and keycaps when rendering. Switches and Keycaps used for rendering are Choc V2 and OLS V1 R3 (Unless ripple), because I found the STEP files for these easily and no other reason.")
display.add_argument('--tray-color', default='0xF0F0F0',
                     help="Color to render the tray with, as a hex number. Default 0xF0F0F0")
display.add_argument('--frame-color', default='0x323232',
                     help="Color to render the frame with, as a hex number. Default 0x323232")
display.add_argument('--mcu-color', default='0x323232',
                     help="Color to render the mcu with, as a hex number. Default 0x323232")
display.add_argument('--switch-color', default='0x323232',
                     help="Color to render the switches with, as a hex number. Default 0x323232")
display.add_argument('--keycap-color', default='0xF0F0F0',
                     help="Color to render the keycaps with, as a hex number. Default 0xF0F0F0")
export.add_argument('--name-suffix', default="",
                    help="Appended to the end of the filenames when exporting stls.")

args = parser.parse_args(sys.argv[1:])

if args.side is None:
    args.side = ['left', 'right']
if args.thumbs == []:
    args.thumbs = ['reachy', 'tucky', 'middle']
if args.pinkies == []:
    args.pinkies = ['upper', 'home', 'lower']

assert not (args.battery == 'none' and args.mcu in [
            'xiao', 'either']), "Read the help message for battery selection."

from src.apiaster_case import make_case, get_mcu, get_switches
from build123d import export_stl, Pos, Rot, mirror, Plane

if 'left' in args.side:
    left_tray, left_frame = make_case(args, left_side=True)

if 'right' in args.side:
    right_tray, right_frame = make_case(args, left_side=False)

if args.export_stl:
    if 'left' in args.side:
        print(f"Export success case/stl/apiaster-left-tray{args.name_suffix}.stl: {export_stl(left_tray, f"case/stl/apiaster-left-tray{args.name_suffix}.stl")}")
        print(f"Export success case/stl/apiaster-left-frame{args.name_suffix}.stl: {export_stl(left_frame, f"case/stl/apiaster-left-frame{args.name_suffix}.stl")}")

    if 'right' in args.side:
        print(f"Export success case/stl/apiaster-right-tray{args.name_suffix}.stl: {export_stl(right_tray, f"case/stl/apiaster-right-tray{args.name_suffix}.stl")}")
        print(f"Export success case/stl/apiaster-right-frame{args.name_suffix}.stl: {export_stl(right_frame, f"case/stl/apiaster-right-frame{args.name_suffix}.stl")}")

if not args.no_show:
    from ocp_vscode import *
    frame_color = int(args.frame_color, 16)
    tray_color = int(args.tray_color, 16)
    mcu_color = int(args.mcu_color, 16)
    keycap_color = int(args.keycap_color, 16)
    switch_color = int(args.switch_color, 16)

    frame_color = ((frame_color >> 16) & 0xFF,
                   (frame_color >> 8) & 0xFF, frame_color & 0xFF)
    tray_color = ((tray_color >> 16) & 0xFF,
                  (tray_color >> 8) & 0xFF, tray_color & 0xFF)
    mcu_color = ((mcu_color >> 16) & 0xFF,
                 (mcu_color >> 8) & 0xFF, mcu_color & 0xFF)
    switch_color = ((switch_color >> 16) & 0xFF,
                    (switch_color >> 8) & 0xFF, switch_color & 0xFF)
    keycap_color = ((keycap_color >> 16) & 0xFF,
                    (keycap_color >> 8) & 0xFF, keycap_color & 0xFF)

    if 'left' in args.side:
        show_object(left_frame, options={
                    "color": frame_color}, name="Left Frame")
        show_object(left_tray, options={"color": tray_color}, name="Left Tray")
        if args.show_more:
            left_mcu = get_mcu(args, left_side=True)
            left_switches = get_switches(args, left_side=True)
            left_keycaps = get_switches(args, left_side=True,keycaps=True)
            show_object(left_mcu, options={
                        "color": mcu_color}, name="Left MCU")
            show_object(left_switches, options={
                        "color": switch_color}, name="Left Switches")
            show_object(left_keycaps, options={
                        "color": keycap_color}, name="Left Keycaps")

    if 'right' in args.side:
        if 'left' in args.side:
            right_tray = Pos(450, 0) * right_tray
            right_frame = Pos(450, 0) * right_frame
        show_object(right_tray, options={
                    "color": tray_color}, name="Right Tray")
        show_object(right_frame, options={
                    "color": frame_color}, name="Right Frame")
        if args.show_more:
            right_mcu = Rot(0, 180, 0) * mirror(get_mcu(args, left_side=False), Plane.XY)
            right_switches = Rot(0, 180, 0) * mirror(get_switches(args, left_side=False), Plane.XY)
            right_keycaps = Rot(0, 180, 0) * mirror(get_switches(args, left_side=False,keycaps=True), Plane.XY)
            if 'left' in args.side:
                right_mcu = Pos(450, 0) * right_mcu
                right_switches = Pos(450, 0) * right_switches
                right_keycaps = Pos(450, 0) * right_keycaps
            show_object(right_mcu, options={
                        "color": mcu_color}, name="Right MCU")
            show_object(right_switches, options={
                        "color": switch_color}, name="Right Switches")
            show_object(right_keycaps, options={
                        "color": keycap_color}, name="Right Keycaps")
