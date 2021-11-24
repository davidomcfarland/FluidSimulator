def VelocityStep(ss, dt, ddv, d2dv2, ddP, Re):
    vx, vy = ss.v
    i,j    = ss.slices[0:2]
    
    box_x, box_y = ss.box_slices

    dvx_dx, dvx_dy, dvy_dx, dvy_dy = ddv
    d2vx_dx2, d2vx_dy2, d2vy_dx2, d2vy_dy2 = d2dv2
    dP_dx, dP_dy = ddP

    # Step Via Navier Stokes
    vx[i,j] = vx[i,j] + dt*(-vx[i,j]*dvx_dx - vy[i,j]*dvx_dy - dP_dx + 1/Re * (d2vx_dx2 + d2vx_dy2))
    vy[i,j] = vy[i,j] + dt*(-vx[i,j]*dvy_dx - vy[i,j]*dvy_dy - dP_dy + 1/Re * (d2vy_dx2 + d2vy_dy2))

    # Boundary Conditions - space
    vx[i,      0] = 0
    vy[i,      0] = 0
    vx[i,ss.Ny-1] = 0
    vy[i,ss.Ny-1] = 0
    vx[0,      :] = -4*ss.U*(ss.y - ss.ystart)*(ss.y - ss.yend)/ss.ylen**2 # Inflow - U is a ss parameter - max Inlet flow velocity
    vy[0,      j] = 0
    vx[ss.Nx-1, j] = vx[ss.Nx-2, j]
    vy[ss.Nx-1, j] = vy[ss.Nx-2, j]

    # Boundary Conditions - box
    vx[box_x, box_y] = 0
    vy[box_x, box_y] = 0

    # enforce changes in ss
    ss.vx = vx
    ss.vy = vy