import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

def tonnage_grade_curve( dfs,var_col,cutoffs=None,weight_col=None,
    as_fraction=True, ylim1=None, ylim2=None, xlim=None, title=None,
    flname=None, xlabel=None,ylabel=None,ylabel2=None,
    fontsize=11,lw=1, figsize=(5,4)):
    '''Generate tonnage-grade curve for one df of multiple dfs. 
    For multiple variables within each df.  

    Args:
        dfs(df or list[df]): Data with a at least one column of values
        var_col (str or list[list[str]]): column-name(s) of variables in a df
        cutoffs(list[float],optional): cut-offs values. If None, 100 cutoffs between
            min-max values are chosen
        weight_col(str,optional): column-name if all dfs with values 
            to weight the grade values. WARINING: Al df's must have the same
            weight_col name.
        as_fraction(bool, optional): If True, it shows tonnage axis as 0-1 fraction.
            If False, shows summ of the weights.
        ylim1(tuple): limit values for main y-axis (weight sum)
        ylim2(tuple): limit values for secondary y_axis (average grades above cutoff)
        xlim(tuple): limit values for x-axis (cutoffs)
        title(str): plot title
        flanme(str): path to store plot. It does not create folders
        fontsize(float): overall font size
        lw(float): line width for GT curves
        figsize(tuple): figsize
    '''
    '''
    TODO:
    - Check what happens when having cutoffs <0
    - Add line for certain cutoffs to check if using/not using cuts works
    - Retrieve the tons and average at certain cutoff table
    - input as array or list of array + variable names
    - add input shape as 4x3 for 12 subplots or 1x1 or 1 for single plot
    - Improve how axis limits of three axes are generated
    - fix when cutoffs given are bigger than actual values. Should auto trim
    '''
    if ylabel2 is None:
        ylabel2 = 'Average'

    if xlabel is None:
        xlabel='Cut-offs'

    #Case 1: dfs is single df
    if isinstance(dfs, pd.DataFrame):
        dfs = [dfs]

        if isinstance(var_col, str):
            var_col = [[var_col]]

        #HOW check all elements in list are lists?
        if isinstance(var_col, list):
            if not all(isinstance(item,list) for item in var_col):
                var_col = [[x] for x in var_col]

    #Case 2: dfs are multiple dfs
    if isinstance(dfs,list):
        if all(isinstance(df,pd.DataFrame) for df in dfs):

            if not isinstance(var_col, list):
                raise ValueError('var_col must be a list')

            if not all(isinstance(x,list) for x in var_col):
                raise ValueError('var_col must be nested list of columns')

            for df in dfs:
                if not all(isinstance(name,str) for ls in var_col
                            for name in ls): 
                    raise ValueError('A var_col name is not in a df')

    #weigth col labels
    if weight_col is not None:
        if as_fraction:
            if ylabel is None:
                ylabel = 'Equally Weighted  (Fraction of Total)'

        if not as_fraction:
            if ylabel is None:
                ylabel = 'Sum of weights'

    #checking all df's
    ylim2_mn = 1E10
    ylim2_mx = -1E10
    
    if weight_col is None:
        weight_col = 'tmp_weight'
        for df in dfs:
            df[weight_col] = 1 

    for i, df in enumerate(dfs):
        #Get global secondary min-max for all df's
        if ylim2 is None:

            if ylim2_mn > df[var_col[i]].to_numpy().min():
                ylim2_mn = df[var_col[i]].to_numpy().min()

            if ylim2_mx < df[var_col[i]].to_numpy().max():
                ylim2_mx = df[var_col[i]].to_numpy().max()

    #plot pars
    legends = []
    colors = ['k','b','r','gray','orange']

    icolor = 0
    fig,ax = plt.subplots(1,1,figsize=figsize)
    secondary=False
    for vars,df in zip(var_col,dfs): 

        arr = df[ vars + [weight_col]].to_numpy()
        #ensure positiveness. seem useless
        arr = arr[ np.all(arr>0, axis=1) ]

        if cutoffs is None:
            #TODO validation why to start in 0 the cutoff
            #subtract to avoid zero len arr. linspace include last one
            cutoffs = np.linspace(0,arr[:,0].max() -1E-7,100)

        #TODO use np.extend because you are looping invalid results?
        tonnage = np.empty(len(cutoffs))
        grade = np.empty(len(cutoffs))

        #sensitivity grades impact tonnage too
        for j,var in enumerate(vars):
            for i, cutoff in enumerate(cutoffs):
                tmp = arr[arr[:,j]>cutoff].copy()

                try:
                    weighted_mean = np.average(tmp[:,j],weights=tmp[:,-1])
                    tonnage_sum = tmp[:,-1].sum()

                    grade[i] = weighted_mean
                    tonnage[i] = tonnage_sum
                except:
                    pass

            if as_fraction:
                tonnage = tonnage / arr[:,-1].sum()

            tmp, = ax.plot(cutoffs,tonnage,lw=lw,c=colors[icolor],label=var)
            #Avoid over-writing axis ticks/labels in bold
            if not secondary:
                ax2 = ax.twinx()
            ax2.plot(cutoffs,grade,linestyle='--',lw=lw,c=colors[icolor])
            legends.append(tmp)
            ax2.set_ylim(ylim2)
            secondary=True

            icolor += 1

    _ = ax2.legend(handles=legends,frameon=False,fontsize=fontsize-1)
    frame = _.get_frame()
    frame.set_edgecolor('k')

    if xlim is None:
        xlim = (min(cutoffs), max(cutoffs))

    if ylim1 is None:
        ylim1 = ( min(tonnage), max(tonnage) )

    _ = ax.set_xlabel(xlabel,fontsize=fontsize)
    _ = ax.set_ylabel(ylabel,fontsize=fontsize)
    _ = ax2.set_ylabel(ylabel2,fontsize=fontsize)

    ax.set_xlim(xlim)
    ax.set_title(title,fontsize=fontsize+1)
    _  = ax.set_ylim(ylim1)

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())


    ax.tick_params(which='major', width=0.5, length=5,color='k')
    ax.tick_params(which='minor', width=0.5, length=3, color='k')

    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.tick_params(which='major', width=0.5, length=5,direction='out')
    ax2.tick_params(which='minor', width=0.5, length=3,direction='out')

    if not as_fraction:
        #add comma to 000's y-axis labels
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(
            lambda x, p: format(int(x), ',')))
    elif as_fraction:
        ax.set_yticks(np.linspace(0,1,6))

    if flname is not None:
        plt.savefig(flname,bbox_inches='tight')
        
#'{:,}'.format(10.005)