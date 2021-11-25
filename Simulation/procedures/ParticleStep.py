from ..libs import plt, mpl
from ..constants import PARTICLE_SHAPE

import numpy as np 
na = np.array
nap = np.append

def ParticleStep(ss, particles, dt, ax, contour=False, P=None):
    ######## Graph output and take a time step

    x_array = na([])
    y_array = na([])
    col_array = na([])
    P_array = na([])

    for p in particles:
        px, py = p.pos
        ## Determine if the particle is out of bounds
        # outside the space
        outLeft    = px < ss.xstart
        outRight   = px > ss.xstart + ss.xlen
        outBottom  = py < ss.ystart
        outTop     = py > ss.ystart + ss.ylen

        # In the box
        inBoxLeft   = px >= ss.box_xstart
        inBoxRight  = px <= ss.box_xend
        inBoxBottom = py >= ss.box_ystart
        inBoxTop    = py <= ss.box_yend

        # combined tests
        out   =   outLeft  or   outRight  or   outBottom  or   outTop
        inBox = inBoxLeft and inBoxRight and inBoxBottom and inBoxTop

        ## Throw out the particle if it is out of bounds
        if out or inBox:
            i = np.where(p==particles)
            particles = np.delete(particles, i)
        ## If the particle is in bounds, plot it and take a time step
        else:
            x_array = nap(x_array, p.pos[0])
            y_array = nap(y_array, p.pos[1])

            col_array = nap(col_array, p.col)
            P_array = nap(P_array, ss.PressureField(*p.pos))

            p.vel = ss.VelocityField(*p.pos)
            p.pos = p.pos + p.vel*dt


    blues = plt.cm.get_cmap("Blues")

    scatter = ax.scatter(x_array, y_array, c=P_array, cmap=blues, norm=ss.norm, marker=PARTICLE_SHAPE, zorder=10)

    # Plot contour lines, if applicable
    if contour:
        yplt, xplt = np.meshgrid(ss.y, ss.x)
        contour_artist = ax.contourf(xplt, yplt, P)
        step_artists = [*contour_artist.collections, scatter]
    else:
        step_artists = [scatter]

    return step_artists