import numpy as np

class space():
    pass

class boundary():
    def __init__(self, point1, point2, orientation="right", closed=True):
        # The points that create the boundary line
        self.point1 = point1
        self.point2 = point2

        # The orientation - which side of the vector from point1 to point2 is "inside" the boundary
        self.orientation = orientation

        # If the boundary is closed or open
        self.closed = closed

    # set the boundary type, if it is valid
    def SetType(self, itype="solid", pair=None): 
        # list of proper type arguments
        available_types = ["periodic", "solid", "terminal"] 
        # if type is valid -> set type -> else raise error
        if itype in available_types:
            # if type is periodic -> ensure the pair attribute has been provided
            if itype == "periodic" and pair==None:
                raise TypeError("Periodic Boundary Conditions require a pair boundary to be provided")
            # set boundary type
            self.type = itype
        else:
            # raise Invalid Boundary Type
            raise TypeError(f"Invalid Boundary type. Valid Boundary Types are : {available_types}")
    
    # Function for Solid Boundary Interactions
    def SolidInteract(self, particle):
        print("FIXME: Solid Boundary Interaction")
    
    # Function for Periodic Boundary Interaction
    def PeriodicInteract(self, particle):
        print("FIXME: Periodic Boundary Interaction") 
    
    # Function for Terminal Boundary Interactions
    def TerminalInteract(self, particle):
        print("FIXME: Terminal Boundary Interaction")

    # Function to Raise Error when an incorrect type or boundary interaction occurs. 
    def ErrorInteract(self, particle):
        raise TypeError("Boundary Type is not valid - Interaction Impossible")

    # Based on the Boundary Type, call the appropriate interaction
    def Interact(self, particle):
        actions = {
            "periodic" : self.PeriodicInteract, 
            "solid"    : self.SolidInteract,
            "terminal" : self.TerminalInteract
        }

        action = actions.get(self.type, self.ErrorInteract)

        action(particle)       

class rectangle(space):
    def __init__(self, xlen=3, ylen=5, xstart=0, ystart=0, Nx=30, Ny=50, U=1, box=None, boundaryTypes="solid"):
        # load arguments into object
        self.xlen = xlen
        self.ylen = ylen
        self.xstart = xstart
        self.ystart = ystart
        self.Nx = Nx
        self.Ny = Ny

        self.xend = xstart + xlen
        self.yend = ystart + ylen

        self.shape = np.array([Nx, Ny])

        # Initialize Grid
        self.x, self.dx = np.linspace(xstart, self.xend, Nx, retstep = True)
        self.y, self.dy = np.linspace(ystart, self.yend, Ny, retstep = True)

        self.xy  = [ self.x,  self.y]
        self.dxy = [self.dx, self.dy]

        self.P = np.zeros(self.shape)

        self.norm = None
        self.cmap = None

        # Initialize Slices - Space
        self.i   = i   = slice(1, Nx-1)
        self.im1 = im1 = slice(0, Nx-2)
        self.ip1 = ip1 = slice(2, Nx)
        self.j   = j   = slice(1, Ny-1)
        self.jm1 = jm1 = slice(0, Ny-2)
        self.jp1 = jp1 = slice(2, Ny)

        self.slices = i, j, im1, ip1, jm1, jp1

        # initialize colorbar
        self.cb = None

        # Initialize optional Box
        if not box==None:
            # read in box parameters
            box_xstart, box_xend, box_ystart, box_yend = box

            # get gridpoints of nearestbox boundaries
            self.box_xstart_index = int((box_xstart - xstart)/self.dx)
            self.box_xend_index   = int((box_xend - xstart)/self.dx)
            self.box_ystart_index = int((box_ystart - ystart)/self.dy)
            self.box_yend_index   = int((box_yend - ystart)/self.dy)

            # round to nearest grid point
            self.box_xstart = self.dx*self.box_xstart_index + xstart
            self.box_xend   = self.dx*self.box_xend_index   + xstart
            self.box_ystart = self.dy*self.box_ystart_index + ystart
            self.box_yend   = self.dy*self.box_yend_index   + ystart

            # wrap up box details
            self.box = [self.box_xstart, self.box_xend, self.box_ystart, self.box_yend]

            # slices for box
            self.box_xslice = slice(self.box_xstart_index, self.box_xend_index)
            self.box_yslice = slice(self.box_ystart_index, self.box_yend_index)

            self.box_slices = [self.box_xslice, self.box_yslice]

        # Initialize Velocities
        self.U = U
        self.vx = -4*self.U*(self.y - self.ystart)*(self.y - self.yend)/self.ylen**2 * np.ones(self.shape)
        self.vy = np.zeros(self.shape)
        self.v = np.array([self.vx, self.vy])

        # create boundaries based on space attributes
        # self.MakeBoundaries()

        # declare boundary types
        # self.SetBoundaryTypes(boundaryTypes)

    def MakeBoundaries(self):
        ## shorter variables for convenience
        xstart, ystart = self.xstart, self.ystart
        xlen, ylen = self.xlen, self.ylen
        ## create counterclockwise vertices
        x1, x2, x3, x4 = xstart, xstart       , xstart + xlen, xstart + xlen
        y1, y2, y3, y4 = ystart, ystart + xlen, ystart + ylen, ystart

        ## create counterclockwise boundaries
        boundary1 = boundary([x1,y1],[x2,y2])
        boundary2 = boundary([x2,y2],[x3,y3])
        boundary3 = boundary([x3,y3],[x4,y4])
        boundary4 = boundary([x4,y4],[x1,y1])

        ## save boundaries as 
        self.boundaries = np.array([boundary1, boundary2, boundary3, boundary4])   
    def SetBoundaryTypes(self, types="solid"):
        if type(types)==type("string"):
            types = [types for i in range(len(self.boundaries))]

        for i in range(len(self.boundaries)):
            try: 
                self.boundaries[i].SetType(types[i])
            except IndexError:
                self.boundaries[i].SetType()

    def PressureField(self, x, y):
        xi = int(np.round((x - self.xstart)/self.dx))
        yi = int(np.round((y - self.ystart)/self.dy))

        try:
            return self.P[xi][yi]
        except:
            raise IndexError("Particle has left Field")
    
    def VelocityField(self, x, y):
        xi = int(np.round((x - self.xstart)/self.dx))
        yi = int(np.round((y - self.ystart)/self.dy))

        try:
            return np.array([self.vx[xi][yi], self.vy[xi][yi]])
        except:
            print(self.vx)
            print(self.xlen, self.ylen)
            print(x,y,xi,yi)
            raise IndexError("Particle has left Field")
            
        




