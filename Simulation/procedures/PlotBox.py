from ..libs import np, plt
from ..constants import BOX_COLOR

def PlotBox(box, ax):
    # unpack variables
    xstart, xend, ystart, yend = box

    # box vertices
    verts = np.array([
        [xstart, ystart],
        [xstart,   yend],
        [  xend,   yend],
        [  xend, ystart]
    ])

    verts_x = verts.T[0]
    verts_y = verts.T[1]

    # plot the lines for each side
    ax.fill(verts_x, verts_y, BOX_COLOR)
