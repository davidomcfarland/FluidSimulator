from ..libs import np

def PressureCalc(ss, dt, ddv, Pold, maxSteps=int(1e4), tol=1e-3):
    dvx_dx, dvx_dy, dvy_dx, dvy_dy = ddv
    i, j, im1, ip1, jm1, jp1 = ss.slices
    
    Nx, Ny = ss.Nx, ss.Ny
    dx, dy = ss.dxy

    bij = (dvx_dx + dvy_dy)/dt - dvx_dx**2 - 2*dvx_dy*dvy_dx - dvy_dy**2

    m = 0
    err = 1

    while (err > tol):
        if m>maxSteps:
            raise RuntimeError("Maximum Pressure Poisson Iterations")
        Pnew = np.copy(Pold)

        dPx_old = Pold[ip1,j] + Pold[im1,j]
        dPy_old = Pold[i,jp1] + Pold[i,jm1]
        bijterm = bij*dx**2*dy**2
        denom   = 2*(dx**2 + dy**2)

        Pnew[i,j] = (dPx_old*dy**2 + dPy_old*dx**2 - bijterm)/(denom)

        # Pressure Boundary Conditions
        Pnew[Nx-1,   :] = 0            # x = Lx: P=0
        Pnew[   :,   0] = Pnew[:,1]    # y = 0 : dP/dy=0
        Pnew[   :,Ny-1] = Pnew[:,Ny-2] # y = Ly: dP/dy=0

        # check if we have converged
        err = np.linalg.norm(Pnew - Pold)/max(1e-8, np.linalg.norm(Pold))
        m += 1

        Pold = Pnew
    
    P = Pnew

    dP_dx = (P[ip1,   j] - P[im1,   j])/(2*dx)
    dP_dy = (P[  i, jp1] - P[  i, jm1])/(2*dy)

    ddP = [dP_dx, dP_dy]

    return P, ddP