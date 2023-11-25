import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class CapAgent():
    '''Class for capping. The class can be instantiated without specific
            parameters. Arguments can be later specified with self.fit() 
            method.
    '''
    '''
    TODO
    - You must choose an option ValueError when calling with 
        all capping dict to None
    - xlim axis are weird using linear and not log xaxis. Why?
    - check if subset is optional. Consider docstring separating optionals
    - add flname? to automatically save img. where?
    -UserWarning: Attempted to set non-positive left xlim on a log-scaled axis.
        Invalid limit will be ignored.
    -due to log scale, this graph is intended for >0 values?
    '''

    def __init__(self,greater_than=None, less_than=None, cap_to=None, 
                subset_col=None,subset_code=None):
        self.greater_than = greater_than
        self.less_than = less_than
        self.cap_to = cap_to
        self.subset_col = subset_col
        self.subset_code = subset_code
        '''Docstring for instance attribute'''

    def fit(self, greater_than=None, less_than=None, cap_to=None,
            subset_col=None,subset_code=None):
        '''Define required capping parameters.

        Args:
            greater_than(float): threshold value
            less_than(float): threshold value
            cap_to(float): capping value
            subset_col(str): column name in pd.DataFrame
            subset_code(int): categorical code

        Returns:
            self: Class object with fitting parameters.
        '''
        '''
        TODO: How to also parse same pars of fit to fit_apply?
        '''
        #check above or below capping
        if all(v is None for v in [greater_than, less_than]):
            raise ValueError('Either a greater_than or less_than value '
                             'must be specified.')
        if not None in [greater_than, less_than]:
            raise ValueError('One of greater_than or less_than '
                             'argument must be specified.')
        
        #check types
        if greater_than is not None:
            if not isinstance(greater_than, (float,int)):
                raise TypeError('greater_than must be float or integer')
        
        if less_than is not None:
            if not isinstance(less_than, (float,int)):
                raise TypeError('less_than must be float or integer')       

        if not isinstance(subset_col, str):
            raise TypeError('subset_col must be a string')           

        if cap_to is None:
            cap_to = [i for i in [greater_than,less_than] if i is not None][0]

        if not isinstance(cap_to, (float,int)):
            raise TypeError('cap_to must be float or integer')    
        
        #TODO what if these were initiated with the Class? add self. retrieval?
        self.greater_than = greater_than
        self.less_than = less_than
        self.cap_to = cap_to
        self.subset_col= subset_col
        self.subset_code = subset_code

        return self

    def fit_apply(self, data, var, suffix='_cap'):
        '''
        Cap values of values in a dataframe column. It requires the fitting
        parameters previously specified with self.fit()

        Args:
            data(pd.DataFrame): df with values
            var(str): column name for values 
        Return:
            None
        '''
        import copy
        data = data.copy()

        self.data = data
        self.var = var

        if self.subset_col is not None:
            orig_vals = data.loc[
                (data[self.subset_col] == self.subset_code) &
                (data[var].notnull())
                ][[var]].copy()
        else:
            orig_vals = data[data[var].notnull()][[var]].copy()
        
        if len(orig_vals) <= 0:
            #TODO is raising error enough
            raise ValueError('There is not enough data')

        #Tracked subset data
        self.idx  = orig_vals.index
        self.orig_vals = orig_vals[var].array

        #Mask-replace
        if self.greater_than:
            self.mask = self.orig_vals > self.greater_than
        else:
            self.mask = self.orig_vals < self.less_than

        capped_vals = self.orig_vals.copy()
        capped_vals[self.mask] = self.cap_to

        self.capped_vals = capped_vals
        self.num_vals = len(self.mask)

        #Add capped with original indexing
        data[f'{var}{suffix}'] = data[var]
        data.loc[self.idx,f'{var}{suffix}'] = self.capped_vals

        self.data = data

        return self #added to chain calling ,fit().fit_apply() 2023-10-26

    def unistats(self, weights=None ,wt_col=None):
        '''Obtain summary statistics of the capped values

        Args:
            weights(np.array): weights for calculating statistics.
                It must be same length than the data.
            wt_col(str): column name in self.data for the weights.
        '''
        if wt_col is None:
            if weights is None:
                weights = np.ones(self.num_vals)/ self.num_vals
            else:
                weights = weights / np.sum(weights)
        else:
            if wt_col in self.data.columns:
                weights = self.data.loc[self.idx, wt_col]
            else:
                raise ValueError('wt_col is not in self.data')

        self.weights = weights
        self.wt_col = wt_col
        #TODO check to avoid negative weights

        summary = dict()
        summary['capped_values'] = dict()

        summary['capped_values'] ['mean'] = np.average(self.capped_vals,weights=self.weights)
        summary['capped_values'] ['std']  = np.sqrt(  np.average( (self.capped_vals- np.average(self.capped_vals, weights=weights))**2, weights=self.weights)   )
        summary['capped_values'] ['cv'] = summary['capped_values'] ['std'] / summary['capped_values'] ['mean']

        summary['capped_values'] ['min']  = np.min(self.capped_vals)
        summary['capped_values'] ['max']  = np.max(self.capped_vals)

        summary['capped_values'] ['q1']  = np.quantile(self.capped_vals,0.25)
        summary['capped_values'] ['median']  = self.capped_vals.median()
        summary['capped_values'] ['q3']  = np.quantile(self.capped_vals,0.75)

        summary['capped_values'] ['cap_to']  = self.cap_to
        summary['capped_values'] ['num_capped']  = self.mask.sum()
        summary['capped_values'] ['frac_capped']  = self.mask.sum() / len(self.mask)
        
        summary['capped_values'] ['diff_mean']  = abs((summary['capped_values'] ['mean'] - np.average(self.orig_vals,weights=self.weights))/ np.average(self.orig_vals,weights=self.weights))

        self.summary = summary
        
    def compare_unistats(self,weights=None, wt_col=None):
        '''Add a record of original_values statistics

        Args:
			weights(np.array,optional): 1-D np.array for the weights.
            wt_col(str,optional): column name in self.data. Only one of
				weights and wt_col parameter must be specified.
        Return:
			None
        '''
        'TODO should this be before or after sensitivity()?'

        if wt_col is None:
            if weights is None:
                weights = np.ones(self.num_vals)/ self.num_vals
            else:
                weights = weights / np.sum(weights)
        else:
            if wt_col in self.data.columns:
                weights = self.data.loc[self.idx, wt_col]
            else:
                raise ValueError

        self.weights = weights
        self.wt_col =wt_col

        #Do a check to avoid negative weights
        self.unistats(weights=self.weights, wt_col = self.wt_col)
        if 'original_values' not in self.summary.keys():
            self.summary['original_values'] = dict()

            self.summary['original_values'] ['mean'] = np.average(self.orig_vals,weights=self.weights)
            self.summary['original_values'] ['std']  = np.sqrt(np.average((self.orig_vals- np.average(self.orig_vals, weights=weights))**2, weights=self.weights))
            self.summary['original_values'] ['cv'] = self.summary['original_values'] ['std'] / self.summary['original_values'] ['mean']

            self.summary['original_values'] ['min']  = self.orig_vals.min()
            self.summary['original_values'] ['max']  = self.orig_vals.max()

            self.summary['original_values'] ['q1']  = np.quantile(self.orig_vals,0.25)
            self.summary['original_values'] ['median']  = self.orig_vals.median()
            self.summary['original_values'] ['q3']  = np.quantile(self.orig_vals,0.75)

    def sensitivity(self, values=None, limit_value=None, weights = None, wt_col=None,
                    chosen_value=None,show_progress=False):
        '''Capping sensitivity analysis over a range of capping values.

        Args:
            values(int or list[float], np.array(float)):
                If int, it is the number of capping values for the sensitivity.
                If list or np.array, it is the values to use for sensitivity
            limit_value(float): If None and capping above a threshold, the limit value
                is the maximum value of uncapped data. If None and capping below a 
                threshold, the limit value is minimum value of uncapped data.
                The limit_value can be also specified by the user.
            weights(np.array): weights for calculating statistics.
                It must be same length than the data.
            wt_col(str): column name in self.data for the weights.
            chosen_value(float): If value is not in values, it is added.
        Return:
            None
        '''
        '''
        TODO
        chose_value should be the one that is in main response or summary
        '''
        from tqdm.notebook import tqdm
        import time 

        if limit_value is None:
            if self.greater_than:
                self.limit_value = self.orig_vals.max()
            else:
                self.limit_value = self.orig_vals.min()
        else:
            self.limit_value = limit_value

        response = dict()

        #TODO if limit_value is sppeficied by the user add a check for it not
        #to be outside of the data range that can raise error. perhaps
        #otput a warning message, trim value to maximum and output this set to maximum value

        #sensitivity_vals 
        if isinstance(values,(float,int)):
            if self.greater_than:
                sensitivity_vals = np.linspace(0,self.limit_value,values)
            elif self.less_than:
                sensitivity_vals = np.linspace(self.limit_value,self.orig_vals.max(),values)

        if isinstance(values,(list,np.ndarray)):
                #TODO further check array dimension, nested lists?
                sensitivity_vals = np.array(values)
                #TODO check this values are within the data range for above / below case

        if values is None:
            values = 250
            if self.greater_than:
                sensitivity_vals = np.linspace(0,self.limit_value,values)
            elif self.less_than:
                sensitivity_vals = np.linspace(self.limit_value,self.orig_vals.max(),values)

        #Add chosen_value to sensitivity values
        if chosen_value is not None:
            if not isinstance(chosen_value,(int,float)):
                raise ValueError('chosen_value must be int or float type')
            self.chosen_value = chosen_value
            sensitivity_vals = np.append(sensitivity_vals,np.array(chosen_value))

        #TODO Loop changes Class'attribute. Better include it in different name
        #Check for better ways
        if self.greater_than and not show_progress:
            #for run, capvalue in enumerate(np.linspace(self.greater_than,self.limit_value,values)):
            for run, capvalue in enumerate(sensitivity_vals):

                #this will set self.cap_to to the last sensitivityvals: how to preserve .fit() capto?
                self.fit(greater_than=capvalue,less_than=None, cap_to=capvalue,
                        subset_col=self.subset_col,subset_code=self.subset_code)

                self.fit_apply(self.data,self.var)    
                self.unistats(weights = weights, wt_col = wt_col)
                response[run] = self.summary['capped_values']
        elif self.less_than and not show_progress:
            #for run, capvalue in enumerate(np.linspace(self.limit_value,self.less_than,values)):
            for run, capvalue in enumerate(sensitivity_vals):

                self.fit(greater_than=None,less_than=capvalue, cap_to=capvalue,
                        subset_col=self.subset_col,subset_code=self.subset_code)

                self.fit_apply(self.data,self.var)    
                self.unistats(weights = weights, wt_col = wt_col)
                response[run] = self.summary['capped_values']

        if self.greater_than and show_progress:
            #for run, capvalue in enumerate(np.linspace(self.greater_than,self.limit_value,values)):
            for run, capvalue in enumerate(tqdm(sensitivity_vals)):

                self.fit(greater_than=capvalue,less_than=None, cap_to=capvalue,
                        subset_col=self.subset_col,subset_code=self.subset_code)

                self.fit_apply(self.data,self.var)    
                self.unistats(weights = weights, wt_col = wt_col)
                response[run] = self.summary['capped_values']
        elif self.less_than and show_progress:
            #for run, capvalue in enumerate(np.linspace(self.limit_value,self.less_than,values)):
            for run, capvalue in enumerate(tqdm(sensitivity_vals)):

                self.fit(greater_than=None,less_than=capvalue, cap_to=capvalue,
                        subset_col=self.subset_col,subset_code=self.subset_code)

                self.fit_apply(self.data,self.var)    
                self.unistats(weights = weights, wt_col = wt_col)
                response[run] = self.summary['capped_values']
            
        self.responses = pd.DataFrame.from_dict(response,orient='index')

    def sensitivity_plot(self,line_at=None,title=None,lw=0.5,figsize=None,xscale='log',
            sinch=(8,6),fontsize=8,ms=1,nbins=None):
        '''Plot a set of four plots for capping sensitivity analysis. 
        Plot a user defined vertical capping line in the graph and 
        show the closest response to that value.

        Args:
            line_at(float): Value to plot a vertical line in the histogram and
                cdf subplots. If summary of the response is shown in the graph, 
                it corresponds to the closest capping value to line_at
            title(str,optional): title of the graph
            lw(float): width of the vertical line plotted at line_at value
            figsize(tuple(float,float)): figure size
            xscale(str): x-scale 'log' or 'linear' for the histogram and cdf
            fontsize(float): font size
            ms(float): marker size for third and fourth subplot
            nbins(int): number of bins for the histogram

        **Examples:**

        .. plot::

            import resourcegeo as rs
            df = rs.BaseData('assay_geo').data
            capped = rs.CapAgent().fit(greater_than=1,cap_to=1,subset_col='rock',subset_code='MXPRI')
            capped.fit_apply(df,'CUpc') 
            capped.sensitivity(values=200, wt_col='ai')
            capped.compare_unistats()
            capped.sensitivity_plot(line_at=1)  

        '''
        import matplotlib.ticker as ticker
        import probscale
        import seaborn as sns

        if title is None:
            title = f"Capping Sensitivity Analysis: {self.subset_col} - {self.var}"

        ylabel = {
            'mean':'Mean',
            'std':'Std. Dev.',
            'mean':'Mean',
            'cv':'Coeffiient of Variation',
            'num_capped':'Number of Capped Data',
            'diff_mean': 'Metal Lost (%)',
            'cap_to':'Capping Value',
        }
        
        delta2font = 1.5
        fontdict={'fontsize':fontsize-delta2font}

        #Plot
        fig, axes = plt.subplots(2,2,figsize=figsize)
        axes= axes.flatten()
        fig.set_size_inches(sinch)

        #First plot
        rmin = self.data[self.var].min()
        if xscale == 'log' and rmin == 0:
            rmin = 0.001
        rmax = self.data[self.var].max()

        if nbins is None:
            nbins = int(np.round(np.sqrt(len(self.orig_vals)),0) + 1)
        if xscale == 'log':
            bins = np.logspace(np.log10(rmin),np.log10(rmax), nbins)
        elif xscale == 'linear':
            bins = nbins

        axes[0].hist(self.orig_vals, bins = bins , edgecolor='white', range =(rmin,rmax), 
                    color = "0.3", weights = self.weights,density=False)
        axes[0].grid(axis = 'both', ls = '-',lw=0.3, zorder=0)

        axes[0].set_xscale(xscale)
        axes[0].set_title(f'Histogram: {self.subset_col}-{self.var}',fontsize=fontsize) 
        axes[0].set_ylabel('Frequency',fontsize=fontsize)
        axes[0].set_xlabel(self.var,fontsize=fontsize)

        if xscale=='log' and self.orig_vals.min()<=0:
            axis_minval = 1E-4
        else:
            axis_minval = self.orig_vals.min()

        formatter = ticker.FormatStrFormatter('%.5g')
        axes[0].xaxis.set_major_formatter(formatter)
        axes[0].set_xlim( (axis_minval, self.orig_vals.max()*2) )

        if xscale == 'log':
            locmaj = ticker.LogLocator(base=10,numticks=20) 
            axes[0].xaxis.set_major_locator(locmaj)
            locmin = ticker.LogLocator(base=10.0,subs=tuple(np.arange(0.1,1,0.1)),numticks=20)
            axes[0].xaxis.set_minor_locator(locmin)
            axes[0].xaxis.set_minor_formatter(ticker.NullFormatter())

        stat_bulk = {
            'Count': f"{len(self.capped_vals)}",
            'Mean':  round(self.summary['original_values']['mean'],3),
            'Std':   round(self.summary['original_values']['std'],3),
            'CoV':   round(self.summary['original_values']['cv'],3),
            'Max':   round(self.summary['original_values']['max'],3),
            'Q3':    round(self.summary['original_values']['q3'],3),
            'Median':round(self.summary['original_values']['median'],3),
            'Q1':    round(self.summary['original_values']['q1'],3),
            'Min':   round(self.summary['original_values']['min'],3),
        }

        #Add summary text
        t = axes[0].text(0.5, 0.35, _describe_helper(pd.Series(stat_bulk))[0], 
                    transform=axes[0].transAxes,fontdict=fontdict)
        t.set_bbox(dict(facecolor='white', alpha=0.3, edgecolor='white'))

        t = axes[0].text(0.5+0.15, 0.35, _describe_helper(pd.Series(stat_bulk))[1], 
                    transform=axes[0].transAxes,fontdict=fontdict)
        t.set_bbox(dict(facecolor='white', alpha=0.3, edgecolor='white'))

        #Second Plot
        probscale.probplot(self.orig_vals, plottype='prob',
                    weights = self.weights,  probax = 'y', markersize=1,
                    scatter_kws = dict(marker='.', linestyle = 'none',
                                        markersize = 0.5),
                    ax = axes[1])
        axes[1].set_ylabel('Probabilities', fontsize=fontsize)
        axes[1].set_ylim(0.01,99.999)
        axes[1].set_xscale(xscale)
        axes[1].grid(True, which="both", ls = '-',lw=0.3)
        axes[1].set_title('Cumulative Probability Plot',fontsize=fontsize)
        axes[1].set_xlabel(self.var,fontsize=fontsize)
        formatter = ticker.FormatStrFormatter('%.5g')
        axes[1].xaxis.set_major_formatter(formatter)
        #axes[1].tick_params(which=u'both',labelsize=fontsize-7)

        if xscale == 'log':
            axes[1].xaxis.set_major_locator(locmaj)
            axes[1].xaxis.set_minor_locator(locmin)
            axes[1].xaxis.set_minor_formatter(ticker.NullFormatter())
        axes[1].set_xlim( (axis_minval,self.orig_vals.max()*2) ) #TODO Weird points beyond reality
        
        #Third Plot
        lbl3_1 = sns.scatterplot(x='cap_to', y = 'mean', 
                                 data = self.responses, 
                                 ax = axes[2], color = 'k', 
                                 linewidth=0,
                                 label = ylabel['mean'], s = ms)
        axes[2].grid(axis = 'x', ls = '--',lw=0.25)
        axes[2].legend(handles=axes[2].lines[:],
                       labels=["Mean"],
                       loc='center left',
                       fontsize=fontsize-delta2font,
                       frameon=False
                       )
        #axes[2].set_title(f"{ylabel['mean']} vs {ylabel['num_capped']}",fontsize=fontsize)
        axes[2].set_title('')
        
        axes[2].set_xlabel(ylabel['cap_to'],fontsize=fontsize)
        axes[2].set_ylabel(ylabel['mean'],fontsize=fontsize)
        axes[2].set_xlim( (self.orig_vals.min(),self.orig_vals.max()) ) 

        ax2sec = axes[2].twinx()
        lbl3_2 = sns.scatterplot(x='cap_to',
                                 y = 'num_capped',
                                 data = self.responses,
                                 color = 'red', 
                                 label = ylabel['num_capped'],
                                 linewidth=0, #to avoid edge overlap
                                 s = ms, ax = ax2sec )   
        ax2sec .legend(handles=ax2sec .lines[:],
                       labels=["Median"],
                       loc='center right',
                       fontsize=fontsize-delta2font,
                       frameon=False)
        ax2sec .grid(axis = 'both', ls = '-',lw=0.3)
        ax2sec.set_ylabel(ylabel['num_capped'],fontsize=fontsize)



        #Fourth plot
        sns.scatterplot(x='cap_to', y = 'cv',
                        data = self.responses,
                        color = 'k', label = 'CoV',
                        linewidth=0,
                        s = ms, ax = axes[3])
        axes[3].set_ylabel(ylabel['cv'],fontsize=fontsize)
        axes[3].set_xlabel(ylabel['cap_to'],fontsize=fontsize)
        axes[3].grid(axis = 'both', ls = '-',lw=0.3)
        
        #axes[3].set_title(f"{ylabel['cv']} vs {ylabel['diff_mean']}",fontsize=fontsize)
        axes[3].set_title('')
        
        axes[3].set_xlim( (self.orig_vals.min(),self.orig_vals.max()) ) 
        axes[3].legend(fontsize=fontsize-delta2font,
                       loc='center left',
                       frameon=False).set_zorder(100)
    
        ax3sec = axes[3].twinx()
        sns.scatterplot(x=self.responses['cap_to'],
                        y = self.responses['diff_mean']*100,color ='red',
                        label =ylabel['diff_mean'],
                        linewidth=0, #to avoid edge overlap
                        s = ms, ax = ax3sec)
        ax3sec.set_ylabel(ylabel['diff_mean'],fontsize=fontsize)
        ax3sec.legend(handles=ax3sec.lines[:], labels=[ylabel['diff_mean']],
                       loc='center right',fontsize=fontsize-delta2font,
                       frameon=False)
        ax3sec.grid(axis = 'both', ls = '-',color='silver',lw=0.3)

        if line_at is None: line_at = self.cap_to
        if line_at is None: line_at = 1E+10
        #Use line_at if within response range
        cond1 = line_at >= self.responses['cap_to'].min()
        cond2 = line_at <= self.responses['cap_to'].max()
        if line_at is not None and all([cond1,cond2]):
            #vertical lines
            for ax in axes:
                ax.axvline(line_at, ls = '--', color = 'tab:orange',
                            linewidth = lw,
                            label = 'Capping Value = ' + str(line_at))   
            axes[1].legend(loc='best',fontsize=fontsize-delta2font)

            #Get closest sensitivity to cap_to
            y = self.responses['cap_to']
            closest_value = min(y, key=lambda x: abs(line_at - x))

            #dict responses at approximated sensitivity value
            response_at = self.responses.loc[
                self.responses['cap_to']==closest_value].to_dict(orient='list')
            response_at = {key:val[0] for key, val in response_at.items()}

            #choose what to print 1
            summary_values = pd.Series(response_at)[
                ['mean','num_capped','frac_capped']]
            names_str, vals_str = _describe_helper(summary_values)
            t = axes[2].text(0.5, 0.15, names_str, 
                        transform=axes[2].transAxes,fontdict=fontdict)
            t.set_bbox(dict(facecolor='white', alpha=0.3, edgecolor='white'))

            t = axes[2].text(0.5+0.3, 0.15, vals_str, 
                        transform=axes[2].transAxes,fontdict=fontdict)
            t.set_bbox(dict(facecolor='white', alpha=0, edgecolor='white'))

            #choose what to print 2
            summary_values = pd.Series(response_at)[['cv','diff_mean']]
            names_str, vals_str = _describe_helper(summary_values)
            t = axes[3].text(0.6, 0.15, names_str, 
                        transform=axes[3].transAxes,fontdict=fontdict)
            t.set_bbox(dict(facecolor='white', alpha=0.3, edgecolor='white'))

            t = axes[3].text(0.6+0.2, 0.15, vals_str, 
                        transform=axes[3].transAxes,fontdict=fontdict)
            t.set_bbox(dict(facecolor='white', alpha=0, edgecolor='white'))

        for ax in axes:
            ax.tick_params(which=u'both', length=2.5, labelsize=fontsize-delta2font)
        ax2sec.tick_params(which=u'both', length=2.5, labelsize=fontsize-delta2font)
        ax3sec.tick_params(which=u'both', length=2.5, labelsize=fontsize-delta2font)

        fig.subplots_adjust(wspace=0.5, hspace=0.3)
        _ =plt.suptitle(title, fontsize=fontsize+delta2font)
        plt.show()
       
def _describe_helper(x):
    '''
    Args:
        x(pd.Series): Values with named indexes
    Return:
        indexes(str): indexes below each other
        values(str): string of values below each other
    '''
    splits = str(x).split()
    indexes, values = "", ""
    for i in range(0, len(splits) - 2, 2):
        indexes += "{:8}\n".format(splits[i])
        values += "{:>8}\n".format(splits[i+1])
    return indexes, values

#TODO ensure the bottom left plot mean is weighted? or not. OR ensure
# that all plots are based on original data not capped? document it in the class
 
#Example
# data = gs.DataFile('cluster.dat').data
# data['Domain'] = [1]*140
# capped = rs.CapAgent().fit(greater_than=2,cap_to=2, subset_col='Domain', subset_code=1) 
# capped.fit_apply(data,var='Primary') 
# capped.sensitivity(values=10, limit_value = None, wt_col = None)
# capped.compare_unistats() #todo check why it goes after sensitivity... fix
# capped.sensitivity_plot(fontsize=10.5,cap_to=50)

# import resourcegeo as rs
# df = rs.BaseData('assay_geo').data
# capped = rs.CapAgent().fit(greater_than=3,subset_col='rock',subset_code='MXPRI').fit_apply(df,'CUpc') 
# capped.sensitivity(values=200, wt_col='ai')
# capped.compare_unistats()
# capped.sensitivity_plot() 