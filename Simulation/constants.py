NUMBER_OF_STEPS                 = 10000     # Number of Simulation Steps
PROGRESS_OUTPUT_FREQ            = 500       # How often to display which step we are on

SIM_X = ( 0, 15)
SIM_Y = (-5, 5)

SIM_GRIDSHAPE = (200, 150 )

REYNOLDS_NUMBER                 = 40        # Reynolds Number
TIMESTEP                        = 2e-4      # Delta t for each simulation step

PARTICLES_PER_INJECTION         = 100       # Number of Visualization Particles to injecT
PARTICLE_STEP_FREQ              = 100       # Frequency of visualization particle steps
PARTICLE_STEPS_PER_INJECTION    = 5         # How often to Inject Visualization Particles
PARTICLE_COLOR                  = "#0047a3" # Color of visualization particles
PARTICLE_SIZE                   = 6         # Markersize in points
PARTICLE_SHAPE                  = "s"       # Particle Shape (Matplotlib abbreviation)

PARTICLE_XSPACING = 2
PARTICLE_YSPACING = 4

BOX_XSTART = 3
BOX_XEND   = 12
BOX_YSTART = -1
BOX_YEND   = 1
BOX_COLOR  = "w"

BOX = [BOX_XSTART, BOX_XEND, BOX_YSTART, BOX_YEND]

# Calculated Constants
PARTICLE_DT = TIMESTEP*PARTICLE_STEP_FREQ