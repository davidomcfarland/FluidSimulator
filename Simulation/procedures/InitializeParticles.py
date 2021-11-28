from ..classes import particle
from ..libs import rand
from ..constants import PARTICLE_SHAPE, PARTICLE_COLOR, PARTICLE_SIZE, PARTICLE_XSPACING, PARTICLE_YSPACING

import numpy as np 
na = np.array
nap = np.append

def InitializeParticles(ss, ax):
    particles = na([])

    hasBox = not ss.box==None

    for i in range(int(ss.Nx/PARTICLE_XSPACING)):
        for j in range(int(ss.Ny/PARTICLE_YSPACING)):
            xi = ss.x[PARTICLE_XSPACING*i]
            yj = ss.y[PARTICLE_YSPACING*j]
            # Determine if the particle is inside the box, if there is a box
            if hasBox:
                box_xstart, box_xend, box_ystart, box_yend = ss.box
                inBox = box_xstart<=xi and xi<=box_xend and box_ystart<=yj and yj<=box_yend
            else:
                inBox = False
            # skip gridspaces inside the box, if there is a box
            if inBox:
                pass
            else:
                # randomly distribute stationary particles around the gridpoints, being careful of the box
                xpos = xi + PARTICLE_XSPACING*rand()*ss.dx
                ypos = yj + PARTICLE_YSPACING*rand()*ss.dy

                pos = [xpos, ypos]
                vel = [0, 0]

                ysp = ss.Ny/PARTICLE_YSPACING

                if j == int((9/16)*ysp) or j == int((7/16)*ysp):
                    col = "#ffffff"
                else:
                    col = PARTICLE_COLOR

                # Create a new particle object, including a matplotlib line object representing it
                newParticle = particle(pos, vel, col)

                # update the particle list
                particles = nap(particles, newParticle)
    #### For-loop over
    return particles