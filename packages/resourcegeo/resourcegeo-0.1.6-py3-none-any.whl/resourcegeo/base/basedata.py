
import pandas as pd
import os

class TabularData: 
    """This class handles tabular data.
    """
    
    def __init__(self, flname=None):
        """
        Args:
            flname (str): Path to read file
            data (pd.DataFrame): values of data
        """
        
        if isinstance(flname,str):
            self.flname = flname
            
        self.data = pd.read_csv(filepath_or_buffer=self.flname)
        # if isinstance(data,pd.DataFrame):
            # self.data = data
            
        # else:
            # if (data is not None) and (not isinstace(data, pd.DataFrame)):
                # try:
                    # self.data = pd.DataFrame(data=data,columns=columns)
                # except:
                    # raise ValueError("Arg data could not be coerced into pd.DataFrame")

def BaseData(fl, griddef=None, **kwargs):
	"""
	Get an example data

	Args:
		testfile (str): available example files below:

		- "assay_geo": assay and lithology 
        - "collar": collar
    Return
	"""

	files = {
		'assay_geo': "assay_geo.csv",
        'collar':"collar.csv"
	}
	if fl not in files:
		raise ValueError(f"{fl} does not exist in database.")

	data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), r'base_data'))
	return TabularData(os.path.join(data_dir, files[fl]), **kwargs)