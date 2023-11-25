'Useful summary plots for drilling data'

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib

def drilling_by_year(df,var,cat,cat2=None,
                     xlabel=None,ylabel=None,
                     title=None,flname=None,
                     figsize=(14,4),
                     cat2_colors=None,legend_loc=None,width=1):
    '''Generates a stacked bar plot by based on a continuous variable
     and two categorical columns. 

    Args:
        df (pd.DataFrame): df with continuous variable
            and two categorical columns 
        var(float): Continuous variable to summarize sums
        cat(str): Column name for categorical that contains a sequence
            of integers to use in the bar chart. e.g. years
        cat2(str): Column name for categorical values to be stacked
        xlabel(str,optional): x-axis label
        ylabel(str,optional): y-axis label
        title(str,optional): title for the plot
        flname(str,optional): path to save image
        figsize(tuple): figure size
        cat2_colors(dict): dictionary for user defined colors. 
        legend_loc(int): position of the legend
        width(float): with of the bars in the bar chart
        
    **Examples:**

    .. plot::

        import resourcegeo as rs
        df = rs.BaseData('collar').data
        drill_type= 'drilltype'
        df.loc[df[drill_type].isna(),drill_type]= 'Undefined'
        rs.drilling_by_year(df,var='length',cat='year',cat2=drill_type,
                   xlabel='Collar year',ylabel='Length Drilled')
    '''
    '''
        TODO: cat was only tested with integers
    -See 
    https://github.com/minillinim/stackedBarGraph
        df.plot(kind=bar) is categorical in nature 
    plt.bar is numerical if number/dates given

    With plt.bar, a second axis for lengths is yet required
    while df.plot(kind=bar) allow length var + stack over cat

    -if cat2colors is given and cat2 no. then it plots different legend
    '''
    if xlabel is None:
        xlabel='Category'

    if ylabel is None:
        ylabel='Accumulated variable by Category'

    if cat2 is None:
        cat2 = 'undefined'
        df[cat2] = 'undefined'
        cat2_colors = {'undefined':'#0047AB'}

    b1 = df.set_index([cat,cat2])
    b2 = b1.groupby(
                level=[cat,cat2],dropna=False).agg(
                Depth_sum = pd.NamedAgg(var, 'sum'),
                Depth_count = pd.NamedAgg(var, 'count'))

    b3 = b2['Depth_sum'].unstack()
    stack_types = b3.columns
    #Force index type due unstack may give float
    df_ = b3.set_index(
        b3.index.astype(int))

    #get missing index to be correct consecutiveness
    nofull_labels = df_.index
    missing = _find_missing(list(nofull_labels))
    missing

    #fill missing rows and sort them
    for miss in missing:
        df_.loc[miss,:] = [np.nan]*len(df_.columns)
    df_ = df_.sort_index()
    labels = df_.index

    #Unstack count for drilling types
    b4 = b2['Depth_count'].unstack()
    for miss in missing:
        b4.loc[miss,:] = [np.nan]*len(b4.columns)
    b4 = b4.sort_index()
    #Get sum acros drilling type columns
    tmp = b4.to_numpy()
    tmp[np.isnan(tmp)] = 0
    xy_val = tmp.sum(axis=1)
    xy_val

    #Get y-coord using depth-sum vals
    tmp = df_.to_numpy().copy() #if not df_ is changed by tmp[]
    tmp[np.isnan(tmp)] = 0
    y = tmp.sum(axis=1)

    #plot
    fig,ax = plt.subplots(1,1,figsize=figsize)
    df_.plot(
        kind='bar',
        stacked=True,
        color=cat2_colors,
        width=width,
        zorder=1,
        ax=ax
        )
    # add count label only if >0
    x_  = [i for i in range(len(xy_val)) if xy_val[i]>0]
    y_ = y[y>0]
    lab_ = xy_val[xy_val>0]
    _addlabels(x_,y_, [int(i) for i in lab_])
    #set position of labels and text
    _ = plt.xticks(x_,nofull_labels)
    #_ = plt.xticks(np.arange(0,len(labels)),labels)

    ax.set_ylim([0,y.max()*1.2])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    #add comma to 000's y-axis labels
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    _ = plt.xticks(rotation=90)
    _ = plt.grid(lw=0.2,c='gray',linestyle='-')
    
    _ = plt.legend().set_zorder(102)
    _ = plt.legend(loc=legend_loc)
    frame = _.get_frame()
    frame.set_edgecolor('black')
    
    if flname:
        plt.savefig(flname,bbox_inches='tight')
    return

def _addlabels(x,y,label):
    for i in range(len(x)):
        plt.text(x[i],  y[i]+50, str(label[i])+' ids',
                va = 'bottom',rotation=90,
                ha='center',fontsize=9,c='k')
def _find_missing(lst):
    return sorted(set(range(lst[0], lst[-1])) - set(lst))


# #DO STATISTICS for collar length and drilling types?
# #Convention name stats_filetype_company_weighting_categorized_variable
# var = 'Date'
# catcol = drill_type_col
# weight_col = 'TD'

# print(collar[catcol].unique())
# cats = ['RC', 'Core', 'Air rotary', 'Oriented Core', 'Dual rotary','Undefined']

# #cats needs to be inferred if not given
# #WEIGHT COL AND VAR cannot be the same column? error multidimensional index?

# #Use depths as weight to get the Length sum
# _ = rs.stats_contvar_cat(
#     collar,
#     var,
#     catcol=catcol,
#     cats=cats,
#     weight_col=weight_col,
#     flname=f'stats_{mine}_unweighted_bycat.csv') 
# display(_)

# #old test for a stacked barplot that didnt work wih plt.bar
# b1 = collar.set_index([cat,cat2])
# b2 = b1.groupby(
#             level=[cat,cat2],dropna=False).agg(
#             Depth_sum = pd.NamedAgg(var, 'sum'),
#             Depth_count = pd.NamedAgg(var, 'count'))
# print(b2.tail(5))

# b4 = b2['Depth_count'].unstack().tail(10)
# print(b4)

# stack_types = b4.columns
# print(stack_types)

# #convert to array and replace nan to avoid nan sum
# import numpy as np
# values = b4.to_numpy()
# values[np.isnan(values)] = 0

# first = np.array([0,0,0,0,0,0,0,0,0,0])
# stack_handler = np.concatenate((first[:,None],values),axis=1)
# stack_handler

# colors = ['r','b','y','g','purple','orange']
# years_labels = [1,2,3,4,5,6,7,8,9,15] #now as number

# for i,name in enumerate(stack_types,1):
#     #sum over different drilltypes to be the stack base
#     stack_base = stack_handler[:,:-1][:,:i].sum(axis=1)
#     type_values = values[:,i-1]

#     _ = plt.bar(years_labels, type_values, bottom =stack_base   
#                 ,color=colors[i-1]
#                 )
# _ = plt.xticks(years_labels)
# _ = plt.legend(stack_types) #seems this align to values