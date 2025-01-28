from build123d import *

DIODE_HEIGHT = 2*MM
__DIODE_HEIGHT_TOL = 0.2*MM
__SMD_DIODE_HEIGHT = 1.2*MM

sod27_diode_combo = (Pos(0,0,.6) * Box(10*MM, 2.6*MM, DIODE_HEIGHT + __DIODE_HEIGHT_TOL + .6,
                  align=(Align.CENTER, Align.CENTER, Align.MAX))) - Box(5*MM, 2.6*MM, .6,
                  align=(Align.CENTER, Align.CENTER, Align.MIN))
sod123_diode_combo = Box(10*MM, 2.6*MM, DIODE_HEIGHT + __DIODE_HEIGHT_TOL,
                  align=(Align.CENTER, Align.CENTER, Align.MAX))
if __name__ == '__main__':
    from ocp_vscode import *
    show_all()
