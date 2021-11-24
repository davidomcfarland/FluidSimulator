from ..libs import np, rand
from ..classes import particle
from ..constants import PARTICLE_SHAPE, PARTICLE_COLOR, PARTICLE_SIZE, PARTICLE_XSPACING, PARTICLE_YSPACING

def InjectParticles(ss, particles, numParticles, ax):
    ######## Drop Particles into grid

    # verticle line at xstart

    xs = ss.xstart*np.ones(int(numParticles/PARTICLE_YSPACING))
    ys = np.linspace(ss.ystart, ss.ystart+ss.ylen, int(numParticles/PARTICLE_YSPACING))
    # create particle objects, with random variation
    for xi, yi in zip(xs, ys):
        # distribute particles around first-line gridpoints with velocities from first-line gridpoints
        pos = np.array([xi + rand()*PARTICLE_XSPACING*ss.dx, yi + rand()*PARTICLE_YSPACING*ss.dy ])
        vel = ss.VelocityField(xi, yi)

        rounded = np.round(np.abs(yi), 2)

        if np.abs(rounded - 0.5) <= 0.2:
            col = "#ffffff"
        else:
            col = PARTICLE_COLOR
        
        # create particle object, including matplotlib representation
        newParticle = particle(pos, vel)
        newParticle.plot_item = ax.plot(*pos, PARTICLE_SHAPE, color=col, markersize=PARTICLE_SIZE)[0]
        
        # append particle to the list
        particles = [*particles, newParticle]
    #

    return particles