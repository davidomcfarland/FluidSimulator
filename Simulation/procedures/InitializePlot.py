from ..libs import plt, mpl

def InitializePlot(ss, figsize=(16,9), facecolor="k"):
    plt.style.use("fast")
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1,16,(1,14), facecolor=facecolor)

    ss.norm = mpl.colors.Normalize(-3,3)
    ss.cmap = plt.cm.get_cmap("viridis")

    plt.xlim(ss.xstart, ss.xend)
    plt.ylim(ss.ystart, ss.yend)

    ax.set_xticks([])
    ax.set_yticks([])

    return fig, ax