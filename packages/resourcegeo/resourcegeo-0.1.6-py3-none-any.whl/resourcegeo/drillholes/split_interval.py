import numpy as np
import pandas as pd
import copy
from .utilities import weighted_avg, weighted_std

def strip_white_spaces(df):
    'delete leading and trailing white spaces on whole df'
    df = df = df.applymap(lambda x: x.strip() 
                          if isinstance(x, str) else x)
    return df

def intervalIntersection(A,B):
#https://stackoverflow.com/questions/69997547/intersections-of-intervals
        ans = []
        i = j = 0
        while i < len(A) and j < len(B):
            # Let's check if A[i] intersects B[j].
            # lo - the startpoint of the intersection
            # hi - the endpoint of the intersection
            lo = max(A[i][0], B[j][0])
            hi = min(A[i][1], B[j][1])
            if lo <= hi:
                ans.append([lo, hi])
            # Remove the interval with the smallest endpoint
            if A[i][1] < B[j][1]:
                i += 1
            else:
                j += 1
        return ans
        
def split_intervals(df1,df2,vars,catcol,ifrom,ito,dh_col,flname=None):
    '''
    Split df1 based on df2 intervals. 

    Args:
        df1(pd.DataFrame or rmsp.IntervalData): table with assay intervals
        df2(pd.DataFrame or rmsp.IntervalData): table with rock intervals
        vars (list or str): variable(s) from df1 . List to be implemented
        catcol (unknown): category column in df2
        ifrom (str): Column in both df1 and df2
        ito (str): Column in both df1 and df2
        dh_col (str): Drillhole column in both df1 and df2
        flname (str): path to store results

    Return:
        Evaluated table. Hardcoded to retrieve some variables based on
        position (Fix)
    '''
    '''
    https://stackoverflow.com/a/61159270 why not use itertuples, iterrows
    TODO: you may have fragments intervals with contiguous same lithology?
            there may be a way to keep them merged
            
    TODO: You dont need one specific catcol. You need only from/tos
          so you can attach as many variables from df2 as desired.
    Dependencies: intervalIntersection
    TODO: (Didn't test the other way around) df2 on df1.
    -not vectorized
    '''
    import pandas as pd 
    import numpy as np
    
    #check types
    if not isinstance(df1, pd.DataFrame):
        raise ValueError("df1 must be pd.DataFrame")
    
    if not isinstance(df2, pd.DataFrame):
        raise ValueError("df2 must be pd.DataFrame")
        
    if isinstance(vars, list):
        if not all(isinstance(x, str) for x in vars):
            try:
                vars = [str(x) for x in vars]
            except:
                raise ValueError("Could not coerce vars elements to str")
        
    if isinstance(vars, str):
        try:
            vars = [str(vars)]
        except:
            raise ValueError('Could not coerce var to str')
            
    
            
    if not isinstance(catcol, str):
        try:
            catcol = str(catcol)
        except:
            raise ValueError('Could not coerce catcol to str')       

    if not isinstance(dh_col, str):
        try:
            dh_col = str(dh_col)
        except:
            raise ValueError('Could not coerce dh_col to str')

    if not isinstance(ifrom, str):
        try:
            ifrom = str(ifrom)
        except:
            raise ValueError('Could not coerce ifrom to str')
            
    if not isinstance(ito,str):
        try:
            ifrom = str(ifrom)
        except:
            raise ValueError('Could not coerce ito to str')
            
    #check existence
    for var in vars:
        if var not in df1.columns:
            raise ValueError(f'{var} is not a column in df1')
        
    if catcol not in df2.columns:
        raise ValueError('catcol is not a column in df2')   
        
    if dh_col not in df1.columns:
        raise ValueError('dh_col is not a column in df1')
        
    if dh_col not in df2.columns:
        raise ValueError('dh_col is not a column in df2')
        
    if ifrom not in df1.columns:
        raise ValueError('ifrom is not a column in df1')
       
    if ito not in df1.columns:
        raise ValueError('ito is not a column in df1')
    
    if ifrom not in df2.columns:
        raise ValueError('ifrom is not a column in df2')
       
    if ito not in df2.columns:
        raise ValueError('ito is not a column in df2')
       
    #reducing columns speed up process. Figure out why
    g1 = df1[[dh_col,ifrom,ito] + vars].copy()
    c2 = df2[[dh_col,ifrom,ito,catcol]].copy()

    g1 = strip_white_spaces(g1)
    c2 = strip_white_spaces(c2)

    #CONVERT ALPH TO DHID CODE. Make a function of it
    int_null = -2147483647
    def get_alph2num_dict(x, int_null):
        '''
        Get dictionary to map alpha -> int
        Args:
            x (pd.DataFrame,pd.Series)
        '''
        import math
        alph2num = {el:i for i,el in 
                zip(range(len(x.unique())),x.unique())}
        
        #correct NaN to integer null

        for key in alph2num.keys():
            state=False
            if not isinstance(key,str):
                if (math.isnan(key)) & (not state):
                    alph2num[key] = int_null
                    state = True
                if (key is None) & (not state):
                    state = True
        return alph2num

    alph2num = get_alph2num_dict(c2[catcol],int_null)
    num2alph = {y:x for x,y in alph2num.items()}
    catnum_col = 'catcode'
    c2[catnum_col] =c2[catcol].map(alph2num)


    slice=False
    result = pd.DataFrame()
    idx=0

    #Use dhs from both c2&g1 despite having data or not
    dhs = np.array(c2[dh_col].to_list() + g1[dh_col].to_list())
    dhs = np.unique(dhs)

    counting = []
    #TODO: if I mix c2+g1 dh codes should i sort alphabetically?

    #It iterates dh codes from c2. There can't be nan dhs in c2. c2 rules
    #LF outputs all dhs from c2 and g1 despite no data in the oher
    not_in_assay=[]
    not_in_litho=[]
    
    ndhs = len(dhs)
    dh_iter = 0
    dh_iter_fac=1
    progress=10
    for dh in dhs:
    
        dh_iter += 1
        if dh_iter >= int(0.1*ndhs):
            print(f'{progress*dh_iter_fac}% of drillholes evaluated')
            dh_iter = 0
            dh_iter_fac += 1

        #TODO dbg_idx not correct?
        dbg_idx =0

        # dh in litho not in assay
        if (dh in c2[dh_col].unique()) & (dh not in g1[dh_col].unique()):
            not_in_assay.append(dh)

            for cat_int in c2[c2[dh_col]==dh].to_dict(orient="records"):
                x1 = cat_int[ifrom]
                x2 = cat_int[ito]
                rock = cat_int[catnum_col]
                rock_dh = cat_int[dh_col]

                grades= [np.nan for var in vars]

                row = np.array([x1,x2,rock] + grades + [rock_dh,dbg_idx])
                cols = [ifrom,ito,catnum_col] + vars + [dh_col,'dbg_idx']
                
                row_df = pd.DataFrame(row.reshape(-1, len(row)),
                    columns=cols)
                if (x2-x1)>0:
                    result = pd.concat([result, row_df])

        #dh in assay not in litho
        if (dh not in c2[dh_col].unique()) & (dh in g1[dh_col].unique()):
            not_in_litho.append(dh)

            for itv in g1[g1[dh_col]==dh].to_dict(orient="records"):
                x1 = itv[ifrom]
                x2 = itv[ito]
                rock = int_null
                rock_dh = itv[dh_col]

                grades= [itv[var] for var in vars]

                row = np.array([x1,x2,rock] + grades + [rock_dh,dbg_idx])
                cols = [ifrom,ito,catnum_col] + vars + [dh_col,'dbg_idx']
                
                row_df = pd.DataFrame(row.reshape(-1, len(row)),
                    columns=cols)
                if (x2-x1)>0:
                    result = pd.concat([result, row_df])
        
        #PERHAPS CAN BE ADDED DH MATCH ALL TO INCREASE SPPED?
        #This root works on intervals with same dhid

        #iterate litho intervals. Nan data in c2 does not matter
        for cat_int in c2[c2[dh_col]==dh].to_dict(orient="records"):
        
            #state of encountered grade interval
            state=False
            
            #This is the problem not getting all records
            #slice to last grade idx before break
            #if slice: 
            #    g1 =  g1.loc[itv.Index:].copy()
                #print(b.Index)

            #Iterate assay ints. Ensure g1 intervals are compared to same c2
            for itv in g1[g1[dh_col]==dh].to_dict(orient="records"):
            #More g1 #columns takes more time. Same #rows. WHY?

                #Interval in play
                itval1 = [[ cat_int[ifrom],cat_int[ito] ]]
                itval2 = [[ itv[ifrom],itv[ito] ]]
                intersect = intervalIntersection(itval1,itval2)
                
                if len(intersect)>0:
                    #aa = (intersect[0][0], intersect[0][1])
                    #counting.append(aa)
                    state = True
                    slice=True

                    #Grade interval belongs rock interval
                    if (itv[ifrom] >= cat_int[ifrom]) & \
                        (itv[ito] <= cat_int[ito]):
                        idx +=1

                        x1 = itv[ifrom]
                        x2 = itv[ito]

                        rock = cat_int[catnum_col]
                        rock_dh = cat_int[dh_col]
                        
                        grades= [itv[var] for var in vars]

                        row = np.array([x1,x2,rock] + grades + [rock_dh,dbg_idx])
                        cols = [ifrom,ito,catnum_col] + vars + [dh_col,'dbg_idx']
                        
                        row_df = pd.DataFrame(row.reshape(-1, len(row)),
                            columns=cols)

                        #This >0 shouldn't be necessary
                        #Check why are we getting zero lengths?
                        if (x2-x1)>0:
                            result = pd.concat([result, row_df])

                    #Grade interval ends after rock interval
                    if (itv[ifrom] >= cat_int[ifrom]) & \
                        (itv[ito] > cat_int[ito]):
                        idx +=1

                        x1 = itv[ifrom]
                        x2 = cat_int[ito]
                        rock = cat_int[catnum_col]
                        rock_dh = cat_int[dh_col]
                        grades= [itv[var] for var in vars]

                        row = np.array([x1,x2,rock] + grades + [rock_dh,dbg_idx])
                        cols = [ifrom,ito,catnum_col] + vars + [dh_col,'dbg_idx']
                        
                        row_df = pd.DataFrame(row.reshape(-1, len(row)),
                            columns=cols)
                        if (x2-x1)>0:
                            result = pd.concat([result, row_df])
                        
                    #Grade interval starts before rock interval
                    if (itv[ifrom] < cat_int[ifrom]) & \
                        (itv[ito] <= cat_int[ito]):
                        idx +=1

                        x1 = cat_int[ifrom]
                        x2 = itv[ito]
                        rock = cat_int[catnum_col]
                        rock_dh = cat_int[dh_col]
                        
                        grades = [itv[var] for var in vars]

                        row = np.array([x1,x2,rock] + grades + [rock_dh,dbg_idx])
                        cols = [ifrom,ito,catnum_col] + vars + [dh_col,'dbg_idx']
                        row_df = pd.DataFrame(row.reshape(-1, len(row)),
                            columns=cols)
                        if (x2-x1)>0:
                            result = pd.concat([result, row_df])

                    #Grade interval surround rock interval
                    if (itv[ifrom] < cat_int[ifrom]) & \
                        (itv[ito] > cat_int[ito]):
                        idx +=1

                        x1 = cat_int[ifrom]
                        x2 = cat_int[ito]
                        rock = cat_int[catnum_col]
                        rock_dh = cat_int[dh_col]
                        grade= [itv[var] for var in vars]

                        row = np.array([x1,x2,rock] + grades + [rock_dh,dbg_idx])
                        cols = [ifrom,ito,catnum_col] + vars + [dh_col,'dbg_idx']
                        row_df = pd.DataFrame(row.reshape(-1, len(row)),
                            columns=cols) #, index=[[idx]]

                        if (x2-x1)>0:
                            result = pd.concat([result, row_df])
                else:
                    # #Add litho that not intersect assay TODO WRONG!
                    # x1 = cat_int[ifrom]
                    # x2 = cat_int[ito]
                    # rock = cat_int[catnum_col]
                    # rock_dh = cat_int[dh_col]

                    # grades= [np.nan for var in vars]

                    # row = np.array([x1,x2,rock] + grades + [rock_dh,dbg_idx])
                    # cols = [ifrom,ito,catnum_col] + vars + [dh_col,'dbg_idx']
                    
                    # row_df = pd.DataFrame(row.reshape(-1, len(row)),
                    #     columns=cols)
                    # if (x2-x1)>0:
                    #     result = pd.concat([result, row_df])

                    #not sure if this works for all cases
                    #break loop if prev. overlap. Reduce grade loop after overlap
                    if state == True:
                        break

            dbg_idx += 1
    
    try:
        result = result.astype({ifrom:float,
                                ito:float,
                                'dbg_idx':float,
                                catnum_col:int #ensure dtype if not fail to remap
                                })
                                
        for var in vars:
            result[var] = result[var].astype(float)
            
    except:
        raise ValueError('Could not coerce output variables float')
                            
    #back to catcol values
    result[catcol] = result[catnum_col].map(num2alph)
    
    result = result.reset_index(drop=True)
    result['ai'] = result[ito] - result[ifrom]
    result = result[[dh_col,ifrom,ito,catcol,'ai',catnum_col] + vars + ['dbg_idx']]
    
    #TODO dbg_idx to be checked
    if flname is not None:
        result.to_csv(flname,index=False)
    return result
        
def split_intervals_deprecated(df1,df2,vars,catcol,ifrom,ito,dh_col,flname=None):
    '''
    Split df1 based on df2. (Didn't test the other way around).
    
    Variables:
    df1(pd.DataFrame or rmsp.IntervalData): table with assay intervals
    df2(pd.DataFrame or rmsp.IntervalData): table with rock intervals

    vars (list or str): variable(s) from df1 . List to be implemented
    catcol (unknown): category column in df2
    ifrom (str): Column in both df1 and df2
    ito (str): Column in both df1 and df2
    dh_col (str): Drillhole column in both df1 and df2

    flname (str): path to store results 

    Output:
        Evaluated table. Hardcoded to retrieve some variables based on
        position (Fix)
    '''
    '''
    TODO: you may have fragments intervals with contiguous same lithology?
            there may be a way to keep them merged
            
    TODO: You dont need one specific catcol. You need only from/tos
          so you can attach as many variables from df2 as desired.
     'https://stackoverflow.com/a/61159270 why not use itertuples, iterrows'
    Dependencies: intervalIntersection
    '''
    import pandas as pd 
    import numpy as np
    
    #check types
    if not isinstance(df1, pd.DataFrame):
        raise ValueError("df1 must be pd.DataFrame")
    
    if not isinstance(df2, pd.DataFrame):
        raise ValueError("df2 must be pd.DataFrame")
        
    if isinstance(vars, list):
        if not all(isinstance(x, str) for x in vars):
            try:
                vars = [str(x) for x in vars]
            except:
                raise ValueError("Could not coerce vars elements to str")
        
    if isinstance(vars, str):
        try:
            vars = [str(vars)]
        except:
            raise ValueError('Could not coerce var to str')
            
    
            
    if not isinstance(catcol, str):
        try:
            catcol = str(catcol)
        except:
            raise ValueError('Could not coerce catcol to str')       

    if not isinstance(dh_col, str):
        try:
            dh_col = str(dh_col)
        except:
            raise ValueError('Could not coerce dh_col to str')

    if not isinstance(ifrom, str):
        try:
            ifrom = str(ifrom)
        except:
            raise ValueError('Could not coerce ifrom to str')
            
    if not isinstance(ito,str):
        try:
            ifrom = str(ifrom)
        except:
            raise ValueError('Could not coerce ito to str')
            
    #check existence
    for var in vars:
        if var not in df1.columns:
            raise ValueError(f'{var} is not a column in df1')
        
    if catcol not in df2.columns:
        raise ValueError('catcol is not a column in df2')   
        
    if dh_col not in df1.columns:
        raise ValueError('dh_col is not a column in df1')
        
    if dh_col not in df2.columns:
        raise ValueError('dh_col is not a column in df2')
        
    if ifrom not in df1.columns:
        raise ValueError('ifrom is not a column in df1')
       
    if ito not in df1.columns:
        raise ValueError('ito is not a column in df1')
    
    if ifrom not in df2.columns:
        raise ValueError('ifrom is not a column in df2')
       
    if ito not in df2.columns:
        raise ValueError('ito is not a column in df2')
       
    #reducing columns speed up process. Figure out why
    g1 = df1[[dh_col,ifrom,ito] + vars].copy()
    c2 = df2[[dh_col,ifrom,ito,catcol]].copy()

    slice=False
    result = pd.DataFrame()
    idx=0
    dhs = c2[dh_col].unique()
    counting = []
    
    for dh in dhs:
        dbg_idx =0
        for cat_int in c2[c2[dh_col]==dh].to_dict(orient="records"):
        
            #state of encountered grade interval
            state=False
            
            #This is the problem not getting all records
            #slice to last grade idx before break
            #if slice: 
            #    g1 =  g1.loc[itv.Index:].copy()
                #print(b.Index)

            for itv in g1[g1[dh_col]==dh].to_dict(orient="records"):
            #More g1 #columns takes more time. Same #rows. WHY?

                #Interval in play
                itval1 = [[ cat_int[ifrom],cat_int[ito] ]]
                itval2 = [[ itv[ifrom],itv[ito] ]]
                intersect = intervalIntersection(itval1,itval2)
                
                if len(intersect)>0:
                    #aa = (intersect[0][0], intersect[0][1])
                    #counting.append(aa)
                    state = True
                    slice=True

                    #Grade interval belongs rock interval
                    if (itv[ifrom] >= cat_int[ifrom]) & \
                        (itv[ito] <= cat_int[ito]):
                        idx +=1

                        x1 = itv[ifrom]
                        x2 = itv[ito]

                        rock = cat_int[catcol]
                        rock_dh = cat_int[dh_col]
                        
                        grades= [itv[var] for var in vars]

                        row = np.array([x1,x2,rock] + grades + [rock_dh,dbg_idx])
                        cols = [ifrom,ito,catcol] + vars + [dh_col,'dbg_idx']
                        
                        row_df = pd.DataFrame(row.reshape(-1, len(row)),
                            columns=cols)

                        #This >0 shouldn't be necessary
                        #Check why are we getting zero lengths?
                        if (x2-x1)>0:
                            result = pd.concat([result, row_df])

                    #Grade interval ends after rock interval
                    if (itv[ifrom] >= cat_int[ifrom]) & \
                        (itv[ito] > cat_int[ito]):
                        idx +=1

                        x1 = itv[ifrom]
                        x2 = cat_int[ito]
                        rock = cat_int[catcol]
                        rock_dh = cat_int[dh_col]
                        grades= [itv[var] for var in vars]

                        row = np.array([x1,x2,rock] + grades + [rock_dh,dbg_idx])
                        cols = [ifrom,ito,catcol] + vars + [dh_col,'dbg_idx']
                        
                        row_df = pd.DataFrame(row.reshape(-1, len(row)),
                            columns=cols)
                        if (x2-x1)>0:
                            result = pd.concat([result, row_df])
                        
                    #Grade interval starts before rock interval
                    if (itv[ifrom] < cat_int[ifrom]) & \
                        (itv[ito] <= cat_int[ito]):
                        idx +=1

                        x1 = cat_int[ifrom]
                        x2 = itv[ito]
                        rock = cat_int[catcol]
                        rock_dh = cat_int[dh_col]
                        
                        grades = [itv[var] for var in vars]

                        row = np.array([x1,x2,rock] + grades + [rock_dh,dbg_idx])
                        cols = [ifrom,ito,catcol] + vars + [dh_col,'dbg_idx']
                        row_df = pd.DataFrame(row.reshape(-1, len(row)),
                            columns=cols)
                        if (x2-x1)>0:
                            result = pd.concat([result, row_df])

                    #Grade interval surround rock interval
                    if (itv[ifrom] < cat_int[ifrom]) & \
                        (itv[ito] > cat_int[ito]):
                        idx +=1

                        x1 = cat_int[ifrom]
                        x2 = cat_int[ito]
                        rock = cat_int[catcol]
                        rock_dh = cat_int[dh_col]
                        grade= [itv[var] for var in vars]

                        row = np.array([x1,x2,rock] + grades + [rock_dh,dbg_idx])
                        cols = [ifrom,ito,catcol] + vars + [dh_col,'dbg_idx']
                        row_df = pd.DataFrame(row.reshape(-1, len(row)),
                            columns=cols) #, index=[[idx]]

                        if (x2-x1)>0:
                            result = pd.concat([result, row_df])
                else:
                    #break loop if prev. overlap. Reduce grade loop after overlap
                    if state == True:
                        break
            dbg_idx += 1
    #result = result.astype({catcol:int})
    
    try:
        result = result.astype({ifrom:float,
                                ito:float,
                                'dbg_idx':float
                                })
                                
        for var in vars:
            result[var] = result[var].astype(float)
            
    except:
        raise ValueError('Could not coerce output variables float')
                            
    result = result.reset_index(drop=True)
    result['ai'] = result[ito] - result[ifrom]
    result = result[[dh_col,ifrom,ito,catcol,'ai'] + vars + ['dbg_idx']]
    
    #TODO dbg_idx to be checked
    #TODO check if catcol is integer or string or doesnt matter
    
    if flname is not None:
        result.to_csv(flname,index=False)
    return result
    