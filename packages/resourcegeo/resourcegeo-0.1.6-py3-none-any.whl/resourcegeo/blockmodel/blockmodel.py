import pandas as pd
import numpy as np
import copy
from .. statistics import utilities
import warnings

class BlockModel():
    '''
    In-progress Block Model Class with some functionalities.

    Args:
        dx(str): dimension in x-direction column
        dy(str): dimension in y-direction column
        dz(str): dimension in z-direction column
    '''
    'TODO: xyz  coords not required at this stage'

    def __init__(self, df, dx, dy, dz):
        
        #Check types
        if not isinstance(df, pd.DataFrame):
            raise ValueError('df must a pandas DataFrame')
        # if not isinstance(x, str):
        #     raise ValueError('Variable x must be a string')
        # if not isinstance(y, str):
        #     raise ValueError('Variable y must be a string')
        # if not isinstance(z, str):
        #     raise ValueError('Variable z must be a string')
        
        if not isinstance(dx, str):
            raise ValueError('Variable dx must be a string')
        if not isinstance(dy, str):
            raise ValueError('Variable dy must be a string')
        if not isinstance(dz, str):
            raise ValueError('Variable dz must be a string')
        
        #Check existance
        column_names = [dx, dy, dz] #x, y, z, 
        for column_name in column_names:
            if column_name not in df.columns:
                raise ValueError(f"{column_name} is not a column in DataFrame")
        
        #Assign attributes
        self.df = df
        # self.x = x
        # self.y = y
        # self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def report(self, vars, density_col,
               mined_out=None, classif_code=None, otype_code=None,
               mass_col='mass',below_cutoff=False):
        '''
        Calculate resource report from a block model. User must ensure
        dx, dy, and dz units meet density_col units. 
        Values < cutoff are trimmed out.

        Args:
            vars(dict/list): If dictionary is given, keys: grade variables 
                             column names.
                             If list is given, items are column names in df
            density_col(str): density column
            mined_out(dict,optional): Key(str): column name of the mined out values.
                Value(list[str or float]): Codes
            classif_code(dict,optional): Key(str): column name for classification values
                Value(list[str or float]): Codes
            otype_code(dict,optional): Key(str): column name of the ore type values
                Value(list[str or float]): Codes
            mass_col(str,optional): column name was mass to be considered in the output

        Return:
            self.summary(pd.DataFrame): Resource reporting
        '''
        '''
        TODO:
        -Convert inpit list of strings e.g. ['Oxd']. Need [['Oxd']]  
        -Add lithological column for domain reporting  
        -Report below cutoff
        -negativ/nan/str should be a check maybe called from each class
        -Volume/mass is tied to the last variable run. Put it in higher level
         of the loop or something to keep it constant based on classification
         same as leapfrog? Do metallic content for each variable as LF?
        '''

        #Check types 
        if not isinstance(vars, (dict,list)):
            raise ValueError(f"{vars} must be dictionary or a list.")
        if isinstance(vars,list):
            vars = {item:{'cutoff':float(0)} for item in vars}   
            warnings.warn('cutoff values are not specified if vars is a list, '\
                          'use dictionary to define cutoffs. '\
                          'Setting zero cutoffs for all items in vars')
            
        for key,val in vars.items():
            if not isinstance(val['cutoff'], (int,float,list)):
                raise ValueError(f"cufoff values must be int, float or list(int or float)")
        
            if isinstance(val['cutoff'], list):
                try:
                    val['cutoff'] = [float(el) for el in val['cutoff']]
                except:
                    raise ValueError(f"Couldn't coerce all {val['cutoff']} to float")
                    
            if isinstance(val['cutoff'], (int,float)):
                val['cutoff'] = [float(val['cutoff'])]
                
        if not isinstance(density_col, str):
            raise ValueError(f"{density_col} must be a string")

        #Check existance
        for var in vars:
            if var not in self.df.columns:
                raise ValueError(f"{var} is not a column in df")
        if density_col not in self.df.columns:
            raise ValueError(f"{density_col} is not a column in DataFrame")

        #Assign attributes
        self.vars = vars
        self.density_col = density_col

        #Check optional variables
        if mined_out is not None:
            if not isinstance(mined_out,dict):
                raise ValueError(f"{mined_out} must be a dict type") 
            if list(mined_out.keys())[0] not in self.df.columns:
                raise ValueError(f"{list(mined_out.keys())[0]} not in df")
            minedout_col = list(mined_out.keys())[0]
        else:
            minedout_col = 'minedout_unknown'
            self.df[minedout_col] = -1
            mined_out = {minedout_col: [[-1]]}
        for test in list(mined_out.values())[0]:
            if not all(x in self.df[minedout_col].unique() for x in test):
                raise ValueError(f"A value in {test} is not in df {minedout_col} column")
        self.mined_out = mined_out
            
        if classif_code is not None:
            if not isinstance(classif_code,dict):
                raise ValueError(f"{classif_code} must be a dict type")
            if list(classif_code.keys())[0] not in self.df.columns:
                raise ValueError(f"{list(classif_code.keys())[0]} not in df")
            classif_col = list(classif_code.keys())[0]
        else:
            classif_col = 'classif_unknown'
            self.df[classif_col] = -1
            classif_code = {classif_col: [[-1]]}
        for test in list(classif_code.values())[0]:
            if not all(x in self.df[classif_col].unique() for x in test):
                raise ValueError(f"A value in {test} is not in df {classif_col} column")
        self.classif_code = classif_code 
            
        if otype_code is not None:
            #type
            if not isinstance(otype_code,dict):
                raise ValueError(f"{otype_code} must be a dict type") 
            #existence of column
            if list(otype_code.keys())[0] not in self.df.columns:
                raise ValueError(f"{list(otype_code.keys())[0]} not in df")
            otype_col = list(otype_code.keys())[0]
        else:
            otype_col = 'otype_unknown'
            self.df[otype_col] = -1
            otype_code = {otype_col: [[-1]]}
        #valid values    
        for test in list(otype_code.values())[0]:
            if not all(x in self.df[otype_col].unique() for x in test):
                raise ValueError(f"A value in {test} is not in df {otype_col} column")
        self.otype_code = otype_code
        
        #Optional assigned variables
        if not isinstance(mass_col, str):
            try:
                mass_col = str(mass_col)
            except:
                raise ValueError(f"Could not coerce {mass_col} to str")
        self.mass_col = mass_col

        #Mass and density col
        self.df2 = self.df.copy()
        self.df2['volume'] = self.df2[self.dx]*self.df2[self.dy]*self.df2[self.dz]
        self.df2[mass_col] = self.df2[self.density_col]*self.df2['volume']

        #Filter by codes and cutoff
        summary = pd.DataFrame()
        for mined in list(self.mined_out.values())[0]:

            otype_cds = list(self.otype_code.values())[0]
            for otype in otype_cds:

                classif_cds = list(self.classif_code.values())[0]
                
                for classif in classif_cds:
                    #Grouping codes
                    tmp = self.df2.loc[
                                (self.df2[minedout_col].isin(mined)) &
                                (self.df2[otype_col].isin(otype)) &
                                (self.df2[classif_col].isin(classif)
                                 )].copy()

                    stats = dict()
                    for var, defs in self.vars.items():
                        for cutoff in defs['cutoff']:

                            #trim by cutoff variable
                            data = tmp[[var,self.mass_col,'volume',
                                        self.density_col]].dropna().copy()
                            if below_cutoff is False:
                                data = data.loc[data[var]>= cutoff].copy()
                            else:
                                data = data.loc[
                                    (data[var]<= cutoff) &
                                    (data[var]>= 0) #TODO check
                                    ].copy()

                            #ensure positive density
                            data = data.loc[data[self.density_col]>0].copy()
                            #TODO record invalid densities
                            
                            x = data[var]
                            weights = data[self.mass_col]
                        
                            #TODO positive mass (dxdydz,density)
                            
                            desc = f'{cutoff:.3f}'
                            if len(x) > 0:
                        
                                stats['volume'] = data['volume'].sum()
                                stats[f'mass']  = weights.sum()
                                stats[f'{var}_cog{desc}'] = [
                                    utilities.weighted_avg(x,weights)]
                            else:
                                stats['volume'] = [np.nan]
                                stats[f'mass']  = [np.nan]
                                stats[f'{var}_cog{desc}'] = [np.nan]
                            
                    stats = pd.DataFrame.from_dict(stats)
                    stats[minedout_col] = [str(mined)]
                    stats[otype_col] = [str(otype)]
                    stats[classif_col] = [str(classif)]
                    summary = pd.concat([summary, stats])
        summary = summary.reset_index(drop=True)
        self.summary = summary
        return self.summary
        
        
    # Parameters:
    # import pandas as pd
    # df = pd.read_csv(f'Example_model.csv')
    # model = rs.BlockModel(df=df,x='X',y='Y',z='Z', dx='dX',dy='dY',dz='dZ')

    # Define parameters
    # vars = {
        # 'SEN02_Ag':{'cutoff':0},
        # 'SEN02_Au':{'cutoff':0},
        # 'SEN02_Pb':{'cutoff':[0,0.5]},
        # 'SEN02_Zn':{'cutoff':0},
        # 'SEN02_AgEq':{'cutoff':[5.97,12.5,1]},
    # } 
    # density_col = 'SG'
    # mined_out = {  
    # 'MinedCode': [[0]]
    # }
    # classif_code = {
        # 'ClassCode':[[2],[2,3],[4],[2,3,4]],
    # }
    # otype_code = {
        # 'TypeCode':[['Oxd'],['Sul'], ['Oxd', 'Sul']],
    # }
    # report = model.report(
            # vars=vars,
            # density_col=density_col,
            # mined_out=mined_out,
            # classif_code=classif_code,
            # otype_code=otype_code
            # )
    # report.to_csv('resource_report.csv',index=False)