from ..libs import np

def VelocityDerivatives(ss):
    vx, vy              = ss.v
    i,j,im1,ip1,jm1,jp1 = ss.slices
    dx, dy              = ss.dxy

    # upwind vx derivatives
    dvx_dx_up = (vx[i,j] - vx[im1,   j])/dx
    dvx_dy_up = (vx[i,j] - vx[  i, jm1])/dy
    # upwind vy derivatives
    dvy_dx_up = (vy[i,j] - vy[im1,   j])/dx
    dvy_dy_up = (vy[i,j] - vy[  i, jm1])/dy
    # centered vx derivatives
    dvx_dx_ce = (vx[ip1,   j] - vx[im1,   j])/(2*dx)
    dvx_dy_ce = (vx[  i, jp1] - vx[  i, jm1])/(2*dy)
    # centered vy derivatives
    dvy_dx_ce = (vy[ip1,   j] - vy[im1,   j])/(2*dx)
    dvy_dy_ce = (vy[  i, jp1] - vy[  i, jm1])/(2*dy)
    # second vx derivatives
    d2vx_dx2 = (vx[ip1,   j] - 2*vx[i,j] + vx[im1,   j])/(dx*dx)
    d2vx_dy2 = (vx[  i, jp1] - 2*vx[i,j] + vx[  i, jm1])/(dy*dy)
    # second vy derivatives
    d2vy_dx2 = (vy[ip1,   j] - 2*vy[i,j] + vy[im1,   j])/(dx*dx)
    d2vy_dy2 = (vy[  i, jp1] - 2*vy[i,j] + vy[  i, jm1])/(dy*dy)

    ddv_up = np.array([dvx_dx_up, dvx_dy_up, dvy_dx_up, dvy_dy_up])
    ddv_ce = np.array([dvx_dx_ce, dvx_dy_ce, dvy_dx_ce, dvy_dy_ce])
    d2dv2  = np.array([ d2vx_dx2,  d2vx_dy2,  d2vy_dx2,  d2vy_dy2])

    ddv = [ddv_up, ddv_ce, d2dv2]

    return ddv