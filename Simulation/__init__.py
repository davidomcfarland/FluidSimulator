from .libs import warnings
from .run import run

warnings.filterwarnings("error")

NUMBER_OF_STEPS         = 100   # Number of Simulation Steps
TIMESTEP                = 2e-4   # Delta t for each simulation step
TIMESTEPS_PER_INJECTION = 1     # How often to Inject Visualization Particles
PARTICLES_PER_INJECTION = 200   # Number of Visualization Particles to injecT
REYNOLDS_NUMBER         = 40    # Reynolds Number