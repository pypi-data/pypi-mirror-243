
class IntervalIntegrity:
    '''In-progress class to check the integrity of drilling data
    such as collar, survey and interval files (assays, lithology).
    '''
    import pandas as pd

    def __init__(self,collar,survey,assay,dhid_col,litho=None):
        #ensure str type and upper case
        try:
            collar = collar.astype({dhid_col:str})
            collar[dhid_col] = collar[dhid_col].str.upper()
        except:
            raise ValueError('Could not coerce dhid_col to str')

        try:
            survey = survey.astype({dhid_col:str})   
            survey[dhid_col] = survey[dhid_col].str.upper()
        except:
            raise ValueError('Could not coerce dhid_col to str')
            
        try:
            assay = assay.astype({dhid_col:str})
            assay[dhid_col] = assay[dhid_col].str.upper()
        except:
            raise ValueError('Could not coerce dhid_col to str')
            
        if litho is not None:
            try:
                litho = litho.astype({dhid_col:str})
                litho[dhid_col] = litho[dhid_col].str.upper()
            except:
                raise ValueError('Could not coerce dhid_col to str')
            

        #CHECK: collar-survey
        collar_ls = set(collar[dhid_col])
        survey_ls = set(survey[dhid_col])
        self.collar_notin_survey = list(collar_ls-survey_ls)
        self.survey_notin_collar = list(survey_ls-collar_ls)

        collarf = strip_white_spaces(collar)
        surveyf = strip_white_spaces(survey)

        collarf_ls = set(collarf[dhid_col])
        surveyf_ls =  set(surveyf[dhid_col])
        self.collarf_notin_surveyf = list(collarf_ls-surveyf_ls)
        self.surveyf_notin_collarf = list(surveyf_ls-collarf_ls)

        summary = dict()
        summary['orig'] = dict()
        summary['orig']['collar_notin_survey'] = self.collar_notin_survey
        summary['orig']['survey_notin_collar'] = self.survey_notin_collar

        summary['post']=dict()
        summary['post']['collar_notin_survey']=self.collarf_notin_surveyf
        summary['post']['survey_notin_collar']=self.surveyf_notin_collarf

        #Here some collar-survey should be deleted
        #or should be in a function of the class

        #CHECK: assay-collar
        assay_ls = set(assay[dhid_col])
        self.assay_notin_collar = list(assay_ls-collar_ls)
        self.collar_notin_assay = list(collar_ls-assay_ls)

        assayf = strip_white_spaces(assay)
        assayf_ls = set(assayf[dhid_col])

        self.assayf_notin_collarf = list(assayf_ls-collarf_ls)
        self.collarf_notin_assayf = list(collarf_ls-assayf_ls)

        summary['orig']['assay_notin_collar'] = self.assay_notin_collar
        summary['orig']['collar_notin_assay'] = self.collar_notin_assay

        summary['post']['assay_notin_collar'] = self.assayf_notin_collarf
        summary['post']['collar_notin_assay'] = self.collarf_notin_assayf

        if litho is not None:
            #CHECK. litho-collar
            litho_ls = set(litho[dhid_col])

            self.litho_notin_collar = list(litho_ls-collar_ls)
            self.collar_notin_litho = list(collar_ls-litho_ls)

            lithof = strip_white_spaces(litho)
            lithof_ls = set(lithof[dhid_col])

            self.lithof_notin_collarf = list(lithof_ls - collarf_ls)
            self.collarf_notin_lithof = list(collarf_ls - lithof_ls)

            summary['orig']['litho_notin_collar'] = self.litho_notin_collar
            summary['orig']['collar_notin_litho'] = self.collar_notin_litho

            summary['post']['litho_notin_collar'] = self.lithof_notin_collarf
            summary['post']['collar_notin_litho'] = self.collarf_notin_lithof

            #CHECK: litho-assay
            self.litho_notin_assay = list(litho_ls - assay_ls)
            self.assay_notin_litho = list(assay_ls - litho_ls)

            self.lithof_notin_assayf = list(lithof_ls - assayf_ls)
            self.assayf_notin_lithof = list(assayf_ls - lithof_ls)

            summary['orig']['assay_notin_litho'] = self.assay_notin_litho
            summary['orig']['litho_notin_assay'] = self.litho_notin_assay

            summary['post']['assay_notin_litho'] = self.assayf_notin_lithof
            summary['post']['litho_notin_assay'] = self.lithof_notin_assayf

        self.summary=summary

    def correct_files(self):
        print('''Correct input files for later use. This functionality is not yet
              implemented''')

def strip_white_spaces(df):
    'delete leading and trailing white spaces on whole df'
    df = df = df.applymap(lambda x: x.strip() 
                          if isinstance(x, str) else x)
    return df


def compare_codes(df1,df2,dhid_col):
    '''Simpler function to compare two changes in
    a column of df1 and df2

    Args:
        df1(pd.DataFrame): DataFrame 1
        df2(pd.DataFrame): DataFrame 2
        dhid_col(str): column name to use'''
    try:
        df1 = df1.astype({dhid_col:str})
        df1[dhid_col] = df1[dhid_col].str.upper()
    except:
        raise ValueError('Could not coerce dhid_col to str')

    try:
        df2 = df2.astype({dhid_col:'object'})
        df2[dhid_col] = df2[dhid_col].str.upper()
    except:
        raise ValueError('Could not coerce dhid_col to str')
        
    df1 = strip_white_spaces(df1)
    df2 = strip_white_spaces(df2)

    #CHECK: df1 vs df2
    df1_ls = set(df1[dhid_col])
    df2_ls = set(df2[dhid_col])
    df1_notin_df2 = list(df1_ls-df2_ls)
    df2_notin_df1 = list(df2_ls-df1_ls)

    summary = dict()
    summary['orig'] = dict()
    summary['orig']['df1_notin_df2'] = df1_notin_df2
    summary['orig']['df2_notin_df1'] = df2_notin_df1

    return summary

def check_difference(df1,df2,col):
    '''Check count and sum difference
    for two dataframes for a specific
    continuous variable column. This
    does not assume that the year of 
    both dfs are consecutive
    
    Args:
    df1(pd.DataFrame): usually new data
    df2(pd.DataFrame): older data
    '''

    smy = pd.DataFrame(
        {'df2':[len(df2[col]),
                df2[col].sum()],
        'df1':[len(df1[col]),
                df1[col].sum()]},
        index=['Count','Sum'])
    smy['frac_diff'] = smy['df1']/smy['df2']-1
    return smy

def delta_year_collar(df,catcol,years,depth_col):
    '''Summary of difference in a single collar file.
    It is not robust as it assumes that the rows
    are unique keys of a DHID
    
    df(pd.DataFrame): dataframe where rows are unique IDs
    catcol(str): column-name for years
    years(list):list of years to consider
    depth_col(str): column-name containing total lengths'''

    res = dict()
    for year in years:
        tmp = df.loc[
            (df[catcol]<=year)]
        count=len(tmp)
        suma = tmp[depth_col].sum()

        res[year]= [count,suma]
    res = pd.DataFrame(res,index=['count','length'])
    return res