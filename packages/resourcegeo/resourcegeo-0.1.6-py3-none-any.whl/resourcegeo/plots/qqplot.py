import matplotlib.pyplot as plt
import numpy as np

def qq_plot( d1,d2,percentiles=None,ms=1,xlim=None,ylim=None,flname=None,
           ylabel=None,title=None, xlabel=None,figsize=None,fontdict=None):
    '''QQ-plot with two given distributions. Lengths of the distributions may
    be different. Alternatively add percentiles and summary stats.

    Args:
        d1(np.array or list[float]): distribution in x-axis
        d2(np.array or list[float]): distribution in y-axis
        percentiles(list[float]): percentiles from 0-100 included
        ms(float): marker size
        xlim(tuple[float]): x-axis limits
        ylim(tuple[float]): y-axis limits
        flname(str): path to save plot
        figsize(tuple(float)): figure size

    Return:
        None
    '''
    if xlabel is None:
        xlabel = 'Reference distribution'

    if ylabel is None:
        ylabel = 'Distribution 2'
    
    if title is None:
        title = 'QQ-plot'

    x = d1.copy()
    y = d2.copy()
    try:
        x = np.array(x)
        y = np.array(y)
    except:
        raise ValueError("Couldn't coerce to np.array")
    x.sort()
    y.sort()

    mx_diag = max(x.max(),y.max())
    mn_diag = min(x.min(),y.min())
    L = 1.E10

    if xlim is None:
        xlim = (mn_diag,mx_diag)
    if ylim is None:
        ylim = (mn_diag,mx_diag)

    #Quantiles or probabilities to use 
    qlx = np.arange(len(x),dtype=float)/len(x)
    qly = np.arange(len(y),dtype=float)/len(y)

    #Use smaller set to control number of points.
    interp = qlx if len(qlx) < len(qly) else qly

    #Values at F-1(z)
    X_ = np.interp(interp,qlx,x)
    Y_ = np.interp(interp,qly,y)  

    fig,ax = plt.subplots(1,1,figsize=figsize)
    ax.scatter(X_,Y_,s=ms,c='k')
    #diagonal
    ax.plot([-L,L],[-L,L],c='k',lw=0.7)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.grid(linestyle='-',lw='0.5')
    plt.xlim(xlim)
    plt.ylim(ylim)

    #Lines for specific quantiles/probabilities
    if percentiles is not None:
        x_pc = np.percentile(x,percentiles)
        y_pc = np.percentile(y,percentiles)
        for i,j,p in zip(x_pc,y_pc,percentiles):
            xs_v = [i,i]
            ys_v = [-L,j]
            xs_h = [-L,i]
            ys_h = [j,j]
            ax.plot(xs_v,ys_v,lw=0.4,c='r',ls='--')
            ax.plot(xs_h,ys_h,lw=0.4,c='r',ls='--')
            #percentile label
            ax.text(mn_diag,j,f'p{p}',c='r',
                    horizontalalignment='left',
                    verticalalignment='bottom')
            
    #Annotate statistics
    xpos = 0.85
    ypos = 0.45
    yoff=0.04
    ha = 'right'

    plt.figtext(xpos,ypos, f'Number of data x: {len(x)}',
                horizontalalignment=ha,fontdict=fontdict)
    plt.figtext(xpos,ypos-yoff,f'mean: {round(x.mean(),3)}',
                horizontalalignment=ha,fontdict=fontdict)
    plt.figtext(xpos,ypos-2*yoff, f'std.dev: {round(x.std(),3)}',
                horizontalalignment=ha,fontdict=fontdict)

    plt.figtext(xpos,ypos-4*yoff, f'Number of data y: {len(y)}',
            horizontalalignment=ha,fontdict=fontdict)
    plt.figtext(xpos,ypos-5*yoff,f'mean: {round(y.mean(),3)}',
            horizontalalignment=ha,fontdict=fontdict)
    plt.figtext(xpos,ypos-6*yoff, f'std.dev: {round(y.std(),3)}',
            horizontalalignment=ha,fontdict=fontdict)
    ax.set_title(title)
    if flname is not None:
        plt.savefig(flname,bbox='tight')