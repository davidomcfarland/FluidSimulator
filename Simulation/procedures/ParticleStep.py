def ParticleStep(ss, particles, dt, ax, contour=False, P=None):
    ######## Graph output and take a time step

    for p in particles:
        px, py = p.pos
        ## Determine if the particle is out of bounds
        # outside the space
        outLeft    = px < ss.xstart
        outRight   = px > ss.xstart + ss.xlen
        outBottom  = py < ss.ystart
        outTop     = py > ss.ystart + ss.ylen

        # In the box
        inBoxLeft   = px >= ss.box_xstart
        inBoxRight  = px <= ss.box_xend
        inBoxBottom = py >= ss.box_ystart
        inBoxTop    = py <= ss.box_yend

        # combined tests
        out   =   outLeft  or   outRight  or   outBottom  or   outTop
        inBox = inBoxLeft and inBoxRight and inBoxBottom and inBoxTop

        ## Throw out the particle if it is out of bounds
        if out or inBox:
            p.plot_item.remove()
            particles.remove(p)
        ## If the particle is in bounds, plot it and take a time step
        else:
            p.plot_item.set_data(*p.pos)

            p.vel = ss.VelocityField(*p.pos)
            p.pos = p.pos + p.vel*dt

    # Plot contour lines, if applicable
    if contour:
        from ..libs import np, plt
        yplt, xplt = np.meshgrid(ss.y, ss.x)

        plt.contourf(xplt, yplt, P)

        if ss.cb:
            ss.cb.remove()
        
        ss.cb = plt.colorbar()