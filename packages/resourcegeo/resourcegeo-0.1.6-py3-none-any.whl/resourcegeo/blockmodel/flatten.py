import pandas as pd
import numpy as np

def closest_node(node, nodes):
    'closest node from a list, to a supplied node'
    from numpy import random
    from scipy.spatial import distance

    closest_index = distance.cdist([node], nodes).argmin()
    return nodes[closest_index]

def project_points(points,bm,keys,xcol,ycol,zcol,
                    projected_axis,offset=0):
    '''Flatten 3D coordinates by re-assigning coordinates of one axis
    towards a major plane (e.g. XY). It uses a dictionary to map
    the flattened coordinates. All keys must be in points keys. 

    Args:
        points(pd.DataFrame): DataFrame containing columns columns for x,y and z
        bm (np.array): array containing multiple xyz coordinates
        keys (dict): Obtained from project_model. Keys: pair of coordinates,
            Values: minimum coordinate at the projected axis
        xcol(str): x-coordinate column in points
        ycol(str): y-coordinate column in points
        zcol(str): z-coordinate column in points
        projected_axis(str): Projection happens perpendicular to this axis
            to the minimum direction. x, y or z
        offset (float): additional delta added after projection
    '''

    if projected_axis not in ['x','y','z']:
        raise ValueError('Projected axis must be x, y or z')

    if projected_axis =='x':
        axp1 = ycol
        axp2 = zcol
        ax_projected = xcol

        coord1= 1
        coord2= 2

    if projected_axis =='y':
        axp1 = xcol
        axp2 = zcol
        ax_projected = ycol

        coord1= 0
        coord2= 2

    if projected_axis =='z':
        axp1 = xcol
        axp2 = ycol
        ax_projected = zcol

        coord1= 0
        coord2= 1

    df = points.copy()
    df = df.reset_index(drop=True)
    pts = df[[xcol,ycol,zcol]].to_numpy()

    #iterator i aligned with reset indexing
    for i,point in enumerate(pts):
        pt = closest_node(point, bm)
        #https://stackoverflow.com/questions/28754603/indexing-pandas-data-frames-integer-rows-named-columns
        #unchained way for column value assignment at specific row index

        df.loc[df.index[i], f'{axp1}_bm'] = pt[coord1]
        df.loc[df.index[i], f'{axp2}_bm'] = pt[coord2]
        
    df[f'{axp1}_str'] = df[f'{axp1}_bm'].astype(str)
    df[f'{axp2}_str'] = df[f'{axp2}_bm'].astype(str)
    df[f'{axp1}{axp2}'] = df[f'{axp1}_str'] + '-' + df[f'{axp2}_str']

    #Map keys and get new coord
    df[f'{ax_projected}_base'] = df[f'{axp1}{axp2}'].map(keys)
    df[f'new_{ax_projected}'] = df[ax_projected] - df[f'{ax_projected}_base'] + offset

    return df

def project_model(grid,xcol,ycol,zcol,projected_axis,offset=0,
                  minimum=True):
    '''Flatten a block model by projecting coordinates of one axis
    (x,y or z) towards a major plane (e.g. XY) in direction of the
    minimum coordinates. The result is a block model flat in a face 
    perpendicular to the direction of projection.

    Args:
        grid (pd.DataFrame): Grid Model
        xcol(str): x-coordinate column in the grid
        ycol(str): y-coordinate column in the grid
        zcol(str): z-coordinate column in the grid
        projected_axis(str): Projection happens perpendicular to this axis
            to the minimum direction. Valids are x, y or z
        offset (float): additional delta added after projection
        min(bool): Projects to the direction of minimum 
                 (if True) or maximum coordinates (if False)

    Return:
        model(pd.DataFrame): Block Model with flattened coordinates
    '''
    import copy

    if projected_axis not in ['x','y','z']:
        raise ValueError('Projected axis must be x, y or z')

    if projected_axis =='x':
        axp1 = ycol
        axp2 = zcol
        ax_projected = xcol

    if projected_axis =='y':
        axp1 = xcol
        axp2 = zcol
        ax_projected = ycol

    if projected_axis =='z':
        axp1 = xcol
        axp2 = ycol
        ax_projected = zcol

    model = grid.copy()

    model[f'{axp1}_str'] = model[axp1].astype(str)
    model[f'{axp2}_str'] = model[axp2].astype(str)
    model[f'{axp1}{axp2}'] = model[f'{axp1}_str'] + '-' + model[f'{axp2}_str']

    if minimum:
        model_pr = model.loc[model.groupby([f'{axp1}{axp2}'])[ax_projected].idxmin()]
    else:
        model_pr = model.loc[model.groupby([f'{axp1}{axp2}'])[ax_projected].idxmax()]

    key2coord = dict(zip(model_pr[f'{axp1}{axp2}'], model_pr[ax_projected]))

    model['y_base'] = model[f'{axp1}{axp2}'].map(key2coord)
    model['new_y'] = model[ax_projected] - model['y_base'] + offset

    return model, key2coord

def upscale_bm(df, grid_in, grid_out,x,y,z,var):
    '''Upscale a block model. It imposes coarse block indexes to
    df coordinates -> xin yin zin = 1. It potentially give (1,0,1) if using
    external coarse blocks outside of df coordinates  

    Args:
        df (pd.DataFrame): 
        grid_in (gs.GridDef): Fine Grid Definition
        grid_out (gs.GridDef): Coarse Grid Definition
        x (str): x-coordinate column in df
        y (str): y-coordinate column in df
        z (str): z-coordinate column in df
        var (str): variable column to average up in df

    Return:
        upscaled (pd.DataFrame): Upscaled model to grid_out.
    '''

    import copy
    dat = df.copy()

    #Get 1D and 3D idxs with grid_in
    fine = grid_in.get_index3d(dat[x],dat[y],dat[z])
    fine1d = grid_in.get_index(dat[x],dat[y],dat[y])

    dat['ix'] = fine[0]
    dat['iy'] = fine[1]
    dat['iz'] = fine[2]
    dat['idx'] = fine1d[0]

    #Get 1D and 3D idxs with grid_out
    coarse = grid_out.get_index3d(dat[x],dat[y],dat[z])
    coarse1d = grid_out.get_index(dat[x],dat[y],dat[z])

    dat['ixo'] = coarse[0]
    dat['iyo'] = coarse[1]
    dat['izo'] = coarse[2]
    dat['idxo'] = coarse1d[0]

    #get minimum and maximum edge coordinates using grid_out
    dat['xloo'] = grid_out.xmn + (dat['ixo']-0.5) * grid_out.xsiz
    dat['xhio'] = dat['xloo'] + grid_out.xsiz

    dat['yloo'] = grid_out.ymn + (dat['iyo']-0.5) * grid_out.ysiz
    dat['yhio'] = dat['yloo'] + grid_out.ysiz

    dat['zloo'] = grid_out.zmn + (dat['izo']-0.5) * grid_out.zsiz
    dat['zhio'] = dat['zloo'] + grid_out.zsiz

    #Check if each x,y,z coarse is within each coarse block edge
    dat['xin'] = 0
    dat['yin'] = 0
    dat['zin'] = 0
    dat['inside']=0
    dat.loc[ (dat[x]>= dat['xloo']) & (dat[x]<= dat['xhio']), 'xin'] = 1
    dat.loc[(dat[y]>= dat['yloo']) & (dat[y]<= dat['yhio'])
            , 'yin'] = 1
    dat.loc[(dat[z]>= dat['zloo']) & (dat[z]<= dat['zhio']),'zin'] = 1
    dat.loc[(dat['xin']==1) & (dat['yin']==1) & (dat['zin']==1),'inside'] = 1

    #grouped coarse idxo key to count insides
    tmp_copy = dat[['idxo','inside']].copy()
    dat_count = tmp_copy.groupby('idxo').count()
    dat_count = dat_count.reset_index()

    #dict key:coarse 1D idx, value: count of grid_in in grid_out cells
    map_in = dict(zip(dat_count['idxo'], dat_count['inside']))
    dat['count'] = dat['idxo'].map(map_in)

    #Fraction filter
    num = 0
    dat_filt = dat.loc[dat['count']>num].copy()
    upscaled = dat_filt.groupby('idxo')[[var]].mean().reset_index()

    #1D -> 3D idx
    idx3 = grid_out.index1d_to_index3d(upscaled['idxo'].to_numpy())
    upscaled['ixo'] = idx3[0]
    upscaled['iyo'] = idx3[1]
    upscaled['izo'] = idx3[2]

    gridout_coords = grid_out.get_coordinates(
        upscaled['ixo'],upscaled['iyo'],upscaled['izo'])
    upscaled['x'] = gridout_coords[0]
    upscaled['y'] = gridout_coords[1]
    upscaled['z'] = gridout_coords[2]

    upscaled = upscaled.drop(['idxo','ixo','iyo','izo'],axis=1)
    #upscaled = upscaled[['x','y','z',var]]

    return upscaled

def gslib2coord(df,var,griddef):
    '''Convert a gslib model into xyz coordinates model. Unlike
    gslib addcoord, it is vectorized.

    Args:
        df(gs.DataFile): GSLIB model
        var(str): variable in df
        griddef(gs.GridDef): grid definition
    '''

    #this gs is gs.DataFile therefore it puts NaN to -999
    dat = df.loc[~df[var].isna()][[var]].copy()
    dat = dat.reset_index() #gslib idx as column
    g = griddef

    #1D -> 3D idx's: index1d_to_index3d gs source
    dat['ix'] = (dat['index'] % (g.nx*g.ny)) % g.nx
    dat['iy'] = (dat['index'] % (g.nx*g.ny)) / g.nx
    dat['iz'] = dat['index'] / (g.nx*g.ny)
    dat = dat.astype({'ix':int,'iy':int,'iz':int})

    #3D idx's -> 3D coordinates 
    dat['x'] = dat['ix']*g.xsiz + g.xmn
    dat['y'] = dat['iy']*g.ysiz + g.ymn
    dat['z'] = dat['iz']*g.zsiz + g.zmn

    dat = dat.drop(['index','ix','iy','iz'],axis=1)
    dat = dat[['x','y','z',var]]

    return dat

def coord2gslib(df,x,y,z,griddef):
    '''Convert an XYZ model into GSLIB model

    Args:
        df(pd.DataFrame):
        x(str): x-coordinate column in df
        y(str): y-coordinate column in df
        z(str): z-coordinate column in df
        griddef(gs.GridDef): Grid definition

    Return:
        gslib_model (pd.DataFrame): GSLIB model where indexes
            align with GSLIB griddefinition
    '''
    import pandas as pd

    dat = df.copy()
    g=griddef
    nxyz = g.nx*g.ny*g.nz

    #add verification if df gslib model meets with griddef

    #From coords to 3d idxs
    dat['ix'] = (dat[x]-g.xmn)/ g.xsiz + 0.5
    dat['ix'] = dat['ix'].apply(np.ceil) -1

    dat['iy'] = (dat[y]-g.ymn)/ g.ysiz + 0.5
    dat['iy'] = dat['iy'].apply(np.ceil) -1

    dat['iz'] = (dat[z]-g.zmn)/ g.zsiz + 0.5
    dat['iz'] = dat['iz'].apply(np.ceil) -1 #for python

    #From 3d idxs to 1d idx
    dat['idx'] = (dat['iz'])*g.nx*g.ny + (dat['iy'])*g.nx + (dat['ix'])

    #sort 1D idxs
    dat = dat.sort_values(by='idx')
    dat = dat.astype({'idx':int})

    #merge full 1d-idx's with non-full bm1 and sort it
    index = pd.DataFrame({'idxs':np.arange(0,nxyz,1)})
    gslib_model = pd.merge(dat,index,how='outer',left_on='idx',right_on='idxs')
    gslib_model = gslib_model.sort_values(by='idxs')

    gslib_model = gslib_model.reset_index(drop=True)
    gslib_model = gslib_model.drop(['ix','iy','iz','idx','idxs'],axis=1)
    
    return gslib_model

 #1.6M (POPULATED)a
 #8.5M (whole grid)

#I cant escape the large nested loop. I could try to decrease one of the loop
# dynamically after finding a point. However, I dont think this is the 
#smartest solution.

#Rather I'd loop the fine grid populated cells and average it locally somahow.
#So the problem would become O(len(finegrid))

#ublkavg is highly inefficient O^2

#Methodology:
# 1. Add 1D and 3D idxs to the fine grid populated model
#The final point model in original spacem requires to be in the GSLIB and written to disk,
#in order to use ublkavg , this is highly expensive procedure for 1x1x1 block
#I will use the coordinates and will give a untranslated griddef

# #From coords to 3d idxs
# kmodel_filt['ixp'] = (kmodel_filt['x']-xmnp)/ xsizp + 0.5
# kmodel_filt['ixp'] = kmodel_filt['ixp'].apply(np.ceil) -1

# kmodel_filt['iyp'] = (kmodel_filt['y_back']-ymnp)/ ysizp + 0.5
# kmodel_filt['iyp'] = kmodel_filt['iyp'].apply(np.ceil) -1

# kmodel_filt['izp'] = (kmodel_filt['z']-zmnp)/ zsizp + 0.5
# kmodel_filt['izp'] = kmodel_filt['izp'].apply(np.ceil) -1 #for python
