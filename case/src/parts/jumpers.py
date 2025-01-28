from build123d import *

__SOLDER_TOL = 1.4*MM

solder_gap = Box(3.4*MM, 2.4*MM, __SOLDER_TOL*2, align=(Align.CENTER,Align.CENTER,Align.CENTER))
if __name__ == '__main__':
    from ocp_vscode import *
    show_object(solder_gap, name="Jumper Solder Gap")
