from .libs import os, plt
from .procedures import *
from .classes import rectangle
from .constants import \
    NUMBER_OF_STEPS, TIMESTEP, REYNOLDS_NUMBER, PARTICLE_STEP_FREQ, PARTICLE_STEP_FREQ,\
    PARTICLE_STEPS_PER_INJECTION, PROGRESS_OUTPUT_FREQ, PARTICLES_PER_INJECTION,\
    PARTICLE_DT, BOX

def run():  
    # Initialize Files
    InitializeFiles()

    # Initialize Simultation Space (ss)
    ss = rectangle(xlen=4, xstart=0, ystart=-5, ylen=10, Nx=100, Ny=250, box=BOX)
    
    # Initialize Plot Objects
    fig = plt.figure(figsize=(16,9))
    ax = plt.axes(facecolor="k")
    
    plt.xlim(ss.xstart, ss.xend)
    plt.ylim(ss.ystart, ss.yend)
    
    #ax.set_xticks([])
    #ax.set_yticks([])

    # Graph box, if applicable
    if not ss.box==None:
        PlotBox(ss.box, ax)

    # initialize particles
    particles = InitializeParticles(ss, ax)

    # Previous Pressure - initialize as none
    Pprev = None
    
    

    for step in range(NUMBER_OF_STEPS):
        # Output step number, if applicable
        if step % PROGRESS_OUTPUT_FREQ == 0:
            print(f"step: {step}")

        # calculate current velocity derivatives
        ddv_up, ddv_ce, d2dv2 = VelocityDerivatives(ss)

        # calculate current Pressure derivatives
        P, ddP = PressureCalc(ss, TIMESTEP, ddv_ce, Pprev)

        # take a Velocity Step
        VelocityStep(ss, TIMESTEP, ddv_up, d2dv2, ddP, REYNOLDS_NUMBER)

        # take a visualization particle step
        if step % PARTICLE_STEP_FREQ == 0:
            fig.canvas.draw_idle()
            particle_step = int(step / PARTICLE_STEP_FREQ)
            if particle_step % PARTICLE_STEPS_PER_INJECTION == 0:
                particles = InjectParticles(ss, particles, PARTICLES_PER_INJECTION, ax)
            ParticleStep(ss, particles, PARTICLE_DT, ax, contour=False, P=P)
            fig.savefig(f"images/step{particle_step}.png")
            

        # prepare for next step
        Pprev = P
    
    # Create Movie
    ffmpeg_file = r"C:\\Users\\mcfarld\\Libs\\ffmpeg-2021-11-15-git-9e8cdb24cd-full_build\\bin\\ffmpeg"

    framerate = 10

    os.system(f"{ffmpeg_file} -framerate {framerate} -i {os.getcwd()}\\images\\step%d.png -pix_fmt yuv420p sim00.mp4")


         

