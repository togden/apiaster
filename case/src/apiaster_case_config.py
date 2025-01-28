from build123d import MM

numbers = {
    'all': ["RC0-2|0-7", "RC0-3|0-8", "RC0-4|0-9", "RC1-0|1-5", "RC0-1|0-6"],
    'reduced': ["RC0-2|0-7", "RC0-3|0-8", "RC0-4|0-9", "RC1-0|1-5", "RCa0-1|0-6"],
    'flex': ["RC0-2|0-7", "RC0-3|0-8", "RC0-4|0-9", "RC1-0|1-5", "RC0-1|0-6", "RCa0-1|0-6"],
}
inner = {
    'all': ["RC2-1|2-6",   "RC2-3|2-8",  "RC4-0|4-5",],
    'reduced': ["RCa2-1|2-6", "RCa2-3|2-8",],
    'flex': ["RC2-1|2-6",   "RC2-3|2-8",  "RC4-0|4-5", "RCa2-1|2-6", "RCa2-3|2-8",]
}
pinky_out = {
    'all': ["RC5-0|0-5", "RC5-1|5-6"],
    'upper-1.5u': ["RC5-0|0-5"],
    'upper-1u': ["RC5-0|0-5"],
    'lower': ["RC5-1|5-6"],
    'none': [],
}
pinky = {'upper': "RC1-3|1-8",  'home': "RC2-4|2-9", 'lower':  "RC3-4|3-9"}
base = [
    "RC1-2|1-7", "RC1-4|1-9", "RC2-0|2-5",
    "RC3-0|3-5", "RC3-1|3-6", "RC3-2|3-7",
    "RC4-3|4-8", "RC4-1|4-6", "RC4-2|4-7",
]
thumbs = {
    'ripple': {
        'reachy': ["RCa5-3|5-8"],
        'tucky': ["RC5-4|5-9"],
        'middle': ["RCa5-2|5-7"]
    },
    'all-1u': {
        'reachy': ["RC5-3|5-8"],
        'tucky': ["RC5-4|5-9"],
        'middle': ["RC5-2|5-7"]
    },
    'classic': {
        'reachy': ["RC5-3|5-8"],
        'tucky': ["RC5-4|5-9"],
        'middle': ["RC5-2|5-7"]
    },
    'flex': {
        'reachy': ["RC5-3|5-8", "RCa5-3|5-8"],
        'tucky': ["RC5-4|5-9"],
        'middle': ["RC5-2|5-7", "RCa5-2|5-7"]
    },
}


# Case Params
BOTTOM_THICKNESS = 3*MM
BOTTOM_THICKNESS_ADJUST = (-0.3*MM, 0.8*MM)
PCB_THICKNESS = 1.6*MM
PCB_SWITCH_SNAPON_DIST = 2.2*MM
CHOC_SWITCH_SNAPON_THICKNESS = 1.5*MM
MX_SWITCH_SNAPON_THICKNESS = 1.5*MM
SIDE_WALL_THICKNESS = 2*MM
CHOC_SWITCH_HEIGHT_ABOVE_PCB = 5.6*MM
MX_SWITCH_HEIGHT_ABOVE_PCB = 10*MM
PCB_EDGE_GAP = 0.4*MM

# USB A Cutout

USB_TOP_PCB_DIST = 7*MM
USB_PORT_DIMS = (12.4*MM, 5.12*MM)

# cable
USB_HEAD_DIMS = (18*MM, 10*MM)
USB_HEAD_TO_PCB = 1.6*MM

# USB C Cutout
# From https://www.lcsc.com/datasheet/lcsc_datasheet_2205251630_Korean-Hroparts-Elec-TYPE-C-31-M-12_C165948.pdf
USBC_PORT_HEIGHT = 3.26*MM
USBC_PORT_LEN = 8.64*MM
USBC_PORT_OFFSET = -3*MM
ABOVE_DIFF_POS = 0*MM

# Designed for 8mm wide 2mm tall
RUBBER_FEET_POSITIONS = [(170, 48), (89, 47),
                         (70, 72), (110, 134), (188, 150)]
RUBBER_FEET_DIAMETER = 8
RUBBER_FEET_DIAMETER_TOL = 0.2
RUBBER_FEET_CUTOUT_DEPTH=0.8
