import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def deviation_plot(x,y, base, flname=None,title=None,y1_label=None,
                       y2_label=None,xlabel=None,hline_label=None,
                       dev_ylim = 0.2):
    '''
    Plot deviations with respect a base value after performing a
    sensitivity analysis.

    Args:
        x (list[float]): x values of the sensitivities
        y (list[float]): results  from the multiple x-values
        base (float): Reference value around where deviation is calculated.
        title(str): title of the graph

    Return:
        None
    '''
    
    #check types
    if not isinstance(x,list):
        try:
            x = list(x)
        except:
            raise ValueError("Could not coerce x to list")
            
    if not isinstance(y,list):
        try:
            y = list(y)
        except:
            raise ValueError("Could not coerce y to list")
            
    if not isinstance(base,float):
        try:
            base = float(base)
        except:
            raise ValueError("Could not base to float")
            
    if len(x) != len(y):
        raise ValueError("x and y must have same length")
    
    
    if title is None:
        title= 'Deviations around reference value'

    if xlabel is None:
        xlabel='Sensitivity values'

    if y1_label is None:
        y1_label = 'Results'

    if y2_label is None:
        y2_label = 'Deviation from base (%)'

    fontsize = 10
    fracoff = dev_ylim # 2nd-axis +/- limits as fraction

    devs = [(i/base-1)*100 for i in y]

    fig, ax = plt.subplots(1,1,figsize=(6,4))
    ax.plot(x,y,c='b',label=y1_label,lw=1)
    ax.set_title(title)
    ax.set_ylabel(y1_label)
    ax.set_xlabel(xlabel, fontsize=fontsize)

    ax.set_ylim(base*(1-fracoff),base*(1+fracoff))
    ax.axhline(base, ls = '--', color = 'tab:red',linewidth = 1, 
            )  
    
    ax.text(1,base,f'Base value:{round(base,2)}',c='r')
    ax.set_xticks(x)
    ax.legend()

    #Second axis
    axsec = ax.twinx()
    axsec.plot(x,devs,
                c='b',ls='-',lw=1)
    axsec.set_ylabel(y2_label)
    axsec.set_ylim(-fracoff*100,fracoff*100)

    ax.tick_params(which=u'both', length=5, labelsize=fontsize-2,
                  direction='out')
    fig.subplots_adjust(wspace=0.3, hspace=0.4)

    if flname is not None:
        plt.savefig(flname,bbox_inches='tight')
    return


# class Test:
    # def __init__(self):
        # self.x=  5 

    # # def __repr__(self):
    # #     return f"HVS and {self.x}"
    # # def __str__(self):
    # #     return "member of Test"
# a = Test()

# # object.__repr__ gives the message in __repr__ as method
# # object.__str__ gives __repr__ message as method
# # object.__str__() gives __str__ message 
# # object.__repr__() gives __repr__ message 

# # print(object) gives __str__ message