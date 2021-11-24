from ..libs import np, plt

# define some point particles
class particle():
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.plot_item = None


        