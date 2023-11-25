import matplotlib.pyplot as plt
import numpy as np

def homotopic_scatter(df,var,ylabel=None,xlabel=None,title=None,
    flname=None,figsize=None):
    '''Plot a scatter showing multivariate variables in y-axis
    
    Variables:
    =========
    df (pd.DataFrame): df with values
    var (str/list[str]): column names

    TODO #check array is all float
    '''
    from matplotlib.ticker import AutoMinorLocator

    if figsize is None:
        figsize=(12,4)

    if xlabel is None:
        xlabel ='Assay record number'

    if ylabel is None:
        ylabel = 'Assayed variable'

    if title is None:
        title = 'Analysis of homotopic assayed data'

    df = df[var].copy()
    df = df.astype(float)
    arr = df.to_numpy()

    nrows = arr.shape[0]
    ncols = arr.shape[1]

    #adhere y-values where values. Flatten to 1D
    for i in range(ncols):
        arr[:,i][~np.isnan(arr[:,i])] = i+1
    Y = arr.reshape(-1)

    #get 1D x-values aligned to Y
    X = []
    for i in range(nrows):
        xaxis_coords = [i+1] * ncols
        X += xaxis_coords

    if len(X) != len(Y):
        raise ValueError('X and Y are not the same size')

    fig,ax = plt.subplots(1,1,figsize=figsize)
    ax.scatter(X,Y,s=0.3,c='k')

    ax.set_ylim((0,ncols+1))
    ax.set_xlim((0,nrows))
    ax.set_title(title)

    ytick_loc = [i+1 for i in range(ncols)]
    _ = ax.set_yticks(ytick_loc,var)
    _ = ax.set_xlabel(xlabel)
    _ = ax.set_ylabel(ylabel)
    ax.xaxis.set_minor_locator(AutoMinorLocator(20))

    if flname is not None:
        plt.savefig(flname,bbox_inches='tight')