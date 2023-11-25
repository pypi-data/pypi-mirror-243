import matplotlib.pyplot as plt

def setup_plot(ax, cbar=None, figsize=None, cax=None, aspect=None):
    '''A small utility function called from many of the plotting functions. This will set up a
    matplotlib plot instance based on whether an axis is passed or not.

    Args:
        ax (mpl.axis): Matplotlib axis to plot the figure
        cbar (bool): Indicate if a colorbar should be plotted or not
        figsize (tuple): Figure size (width, height)
        cax: Matplotlib.ImageGrid.cbar_axes object
        aspect (bool, str, float): Bool for creating axes, str or float
            for existing axes

    Return:
        fig (mpl.plt.fig): Matplotlib figure
        ax (mpl.axis): Matplotlib axis to plot the figure
        cax: Matplotlib.ImageGrid.cbar_axes object
    '''
    from mpl_toolkits.axes_grid1 import ImageGrid

    if ax is None:
        # Setup up a new plot
        fig = plt.figure(figsize=figsize)
        cbar_mode = None
        if cax is None:
            if cbar: cbar_mode = 'single'
        if aspect is None: aspect = True
        
        imggrid = ImageGrid(fig, 111, nrows_ncols=(1, 1), axes_pad=0.07,
                            cbar_mode=cbar_mode, cbar_size=0.075, aspect=aspect)
        
        #get one ax from the imagegrid
        ax = imggrid[0]
        if cax is None:
            cax = imggrid.cbar_axes[0]
    elif hasattr(ax, "cax"):
        cax = ax.cax
        fig = plt.gcf()
    # elif cbar:
    #     try:
    #         fig, cax = get_cbar_axis(ax, cax)
    #     except:
    #         fig = plt.gcf()
    #         if hasattr(ax, 'cax'):
    #             cax = ax.cax
    #         if cax is None:
    #             raise ValueError("A colorbar axes `cax` must be passed as the passed `ax` cannot be"
    #                             " divided.")
    else:
        fig = plt.gcf()

    return fig, ax, cax

def probability_plot(data,figsize=None,xscale='log',fontsize=10,ms=1,ax=None,
                     label=None,color=None,xlim=None,title=None, xlabel=None,
                     ylabel=None):
    '''Creates a probability plot of an input distribution. 

    Args:
        data: input data to plot
        figsize(tuple): Figure size
        xscale(str): x-axis scale, it can be 'log' or 'linear'

    **Examples:**

	.. plot::

		import resourcegeo as rs
		df = rs.BaseData('assay_geo').data
		_ = rs.probability_plot(df['CUpc'])
    '''
    '''
    TODO probscale accepts weights, enable it
    '''
    import probscale
    import matplotlib.ticker as ticker

    if title is None: title = 'Probability Plot'
    if xlabel is None:  xlabel = 'Variable'
    if ylabel is None:  ylabel = 'Probabilities'

    #set axis
    _, ax, _ = setup_plot(ax, figsize=figsize, aspect=False)

    xmn = data.min()

    if xlim is None and xscale=='log':
        if xmn <= 0: xmn = 1E-3
        xlim = (xmn,data.max())
        
    if xlim is None and xscale != 'log':
        xlim = (xmn,data.max())

    #plot
    probscale.probplot(data, plottype='prob', weights = None, 
                       probax = 'y', scatter_kws = dict(marker='.', linestyle = 'none',
                       markersize = ms,c=color),
                       label=label,ax = ax)
    
    #appearance
    ax.set_ylim(0.001,99.99)
    ax.set_xscale(xscale)
    ax.grid(True, which="both", ls = '-',lw=0.7)
    ax.set_title(title,fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.set_xlabel(xlabel,fontsize=fontsize)

    if label is not None:
        ax.legend()

    ax.tick_params(which=u'both',labelsize=fontsize,length=2)
    _ = plt.yticks(fontsize=7)
    _ = ax.set_xlim(xlim)

    return ax