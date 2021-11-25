from .libs import os, time, ArtistAnimation, mpl, plt
from .procedures import \
    InitializeFiles, InitializePlot, VelocityDerivatives, PressureCalc, PlotBox, InjectParticles,\
    ParticleStep, VelocityStep, InitializeParticles
from .classes import rectangle
from .constants import \
    NUMBER_OF_STEPS, TIMESTEP, REYNOLDS_NUMBER, PARTICLE_STEP_FREQ, PARTICLE_STEP_FREQ,\
    PARTICLE_STEPS_PER_INJECTION, PROGRESS_OUTPUT_FREQ, PARTICLES_PER_INJECTION,\
    PARTICLE_DT, BOX

import numpy as np 

na = np.array
nap = np.append

def run():  
    totalTime = time()
    # Initialize Files
    
    InitializeFiles()

    # Initialize Simultation Space (ss)
    ss = rectangle(xlen=4, xstart=0, ystart=-5, ylen=10, Nx=100, Ny=250, box=BOX)
    
    # Initialize Plot Objects
    fig, ax = InitializePlot(ss)

    # Graph box, if applicable
    if not ss.box==None:
        PlotBox(ss.box, ax)

    # initialize particles
    particles = InitializeParticles(ss, ax)

    # Previous Pressure - initialize as none
    Pprev = None

    stepsTime = time()
    total_particle_time = 0

    artists = list([])
    
    for step in range(NUMBER_OF_STEPS):
        # Output step number, if applicable
        if step % PROGRESS_OUTPUT_FREQ == 0:
            print(f"step: {step}")

        # calculate current velocity derivatives
        ddv_up, ddv_ce, d2dv2 = VelocityDerivatives(ss)

        # calculate current Pressure derivatives
        P, ddP = PressureCalc(ss, TIMESTEP, ddv_ce, Pprev)

        ss.P = P

        # take a Velocity Step
        VelocityStep(ss, TIMESTEP, ddv_up, d2dv2, ddP, REYNOLDS_NUMBER)

        # take a visualization particle step
        if step % PARTICLE_STEP_FREQ == 0:
            particle_time = time()
            particle_step = int(step / PARTICLE_STEP_FREQ)
            if particle_step % PARTICLE_STEPS_PER_INJECTION == 0:
                particles = InjectParticles(ss, particles, PARTICLES_PER_INJECTION, ax)
            step_artists = ParticleStep(ss, particles, PARTICLE_DT, ax, contour=True, P=P)
            artists.append(step_artists)
            total_particle_time += time() - particle_time

        # prepare for next step
        Pprev = P
    print(f"step: {NUMBER_OF_STEPS}")
    print(f"Iteration Steps Complete\n\n")
    stepsTime = time()-stepsTime
    
    movieTime = time()
    # Create Movie

    print("writing movie files")

    ani = ArtistAnimation(fig, artists, interval=100, blit=True)

    newNorm = mpl.colors.Normalize(ss.P.min(), ss.P.max())

    cax = fig.add_subplot(1,16,16)

    ScalarMap = plt.cm.ScalarMappable(norm=newNorm, cmap=ss.cmap)
    plt.colorbar(mappable=ScalarMap, cax=cax, fraction=1)

    for artist in artists:
        for collection in artist:
            collection.norm = newNorm

    ani.save("sim03.mp4")

    movieTime = time() - movieTime
    totalTime = time() - totalTime
    
    print(f"Total Runtime:\n\t{totalTime}")
    print(f"Total Steps Time:\n\t{stepsTime}")
    print(f"Avg Steps Time:\n\t{stepsTime/NUMBER_OF_STEPS}")
    print(f"Total Particle Time:\n\t{total_particle_time}")
    print(f"Avg Particle Time:\n\t{total_particle_time*PARTICLE_STEP_FREQ/NUMBER_OF_STEPS}")
    print(f"Movie Time:\n\t{movieTime}")
