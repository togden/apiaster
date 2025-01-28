from build123d import *


cut_main = Pos(0,-2.5)*Box(11,11,1, align=(Align.CENTER,Align.CENTER,Align.MAX))
cut_top = Pos(0,-2.5)*Box(3,11,1, align=(Align.CENTER,Align.CENTER,Align.MIN))
if __name__ == '__main__':
    from ocp_vscode import *
    show_all()
