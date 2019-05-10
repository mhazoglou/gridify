from __future__ import division
import numpy as np
from scipy import ndimage as ndim
import matplotlib.image as mpimg

def gridify(inputfile, outputfile, center, pix_per_grid_shape,\
            dpi, threshold=0.5):
    """
    inputfile - is a string containing the path and extension of
    the input png file

    outputfile - is a string containing the path and extension of
    the output png file

    center - tuple containing the coordinates of the grid origin
    specified as (col, row) or (x, y) where y is verticle position
    as measured from the top of the image and x the horizontal
    position as measured from the left of the image

    pix_per_grid_shape - tuple specifying grid size in pixel e.g.
    (10, 20) for 10 pixels in width (horizontal/colums) and 20 in
    length (verticle/rows)

    dpi - dots per inch printing resolution

    threshold - value between 0 and 1 the criteria for making a
    patch in the pattern into a grid. The default is 0.5 meaning
    if half or more of then half of the pixels in the pattern are
    inside the patch it will become a grid block
    """
    
    im = mpimg.imread(inputfile, format='png')
    edge_array = np.logical_not(\
        np.floor(im[:,:,0]+im[:,:,1]+im[:,:,2]).astype(bool))
    
    shape = edge_array.shape
    lenY, lenX = shape
    
    row_loc, col_loc = np.nonzero(edge_array)
    unique_row_loc = list(np.unique(row_loc))

    #filling in the shape of the pattern
    fill_edge_array = np.zeros(shape, dtype = bool)
    for row in unique_row_loc:
        cols = col_loc[np.equal(row_loc, row)]
        col_idx_space = np.argwhere(cols[1:]-cols[:-1] > 1)
        N_spaces = len(col_idx_space)
        if N_spaces < 2:
            min_col = min(cols)
            max_col = max(cols)
            fill_edge_array[row, min_col:max_col+1] = True
        elif (N_spaces % 2 != 0):
            fill = False
            prev_space = 0
            idx_space_List = [x[0] for x in col_idx_space.tolist()] + [-1]
            for idx_space in idx_space_List:
                fill_edge_array[row, cols[prev_space]:cols[idx_space]] = fill
                fill = not fill
                prev_space = idx_space
        else:
            min_col = min(cols)
            max_col = max(cols)
            fill_edge_array[row, min_col:max_col+1] = True
    
    center_x, center_y = center
    pix_per_grid_x, pix_per_grid_y = pix_per_grid_shape

    # initializing the grid pattern with a boolean array
    # lenX-center_x-1 requires the minus one because otherwise the centers index is not accounted
    gx = np.arange(\
        -pix_per_grid_x*(center_x//pix_per_grid_x),\
        pix_per_grid_x*((lenX-center_x-1)//pix_per_grid_x)+1,\
        pix_per_grid_x)
    gy = np.arange(\
        -pix_per_grid_y*(center_y//pix_per_grid_y),\
        pix_per_grid_y*((lenY-center_y-1)//pix_per_grid_y)+1,\
        pix_per_grid_y)
    y_grid_idx = center_y + gy
    x_grid_idx = center_x + gx
    basic_grid = np.zeros(shape, dtype=bool)
    basic_grid[y_grid_idx, :] = True
    basic_grid[:, x_grid_idx] = True


    #pixelating the edges of fill_edge_array by scheme
    y_grid_list = list(y_grid_idx)
    if 0 not in y_grid_list:
        y_grid_list = [0] + y_grid_list

    x_grid_list = list(x_grid_idx)
    if 0 not in x_grid_list:
        x_grid_list = [0] + x_grid_list

    tot_y_grids = len(y_grid_list)
    tot_x_grids = len(x_grid_list)
    n_pix_per_grid = pix_per_grid_x*pix_per_grid_y
    for idxL_y in xrange(tot_y_grids):
        y_start = y_grid_list[idxL_y]
        if idxL_y+1 < tot_y_grids:
            y_end = y_grid_list[idxL_y+1]
        else:
            y_end = None
        for idxL_x in xrange(tot_x_grids):
            x_start = x_grid_list[idxL_x]
            if idxL_x+1 < tot_x_grids:
                x_end = x_grid_list[idxL_x+1]
            else:
                x_end = None
            section = fill_edge_array[y_start:y_end, x_start:x_end]
            tot = np.sum(section)
            if tot/n_pix_per_grid >= threshold:
                if y_end == None and x_end == None:
                    fill_edge_array[y_start:y_end, x_start:x_end] = True
                elif y_end == None:
                    fill_edge_array[y_start:y_end, x_start:(x_end+1)] = True
                elif x_end == None:
                    fill_edge_array[y_start:(y_end+1), x_start:x_end] = True
                else:
                    fill_edge_array[y_start:(y_end+1), x_start:(x_end+1)] = True
            else:
                if y_end == None and x_end == None:
                    fill_edge_array[y_start+1:y_end, x_start+1:x_end] = False
                elif y_end == None:
                    fill_edge_array[y_start+1:y_end, x_start+1:(x_end+1)] =\
                                                     False
                elif x_end == None:
                    fill_edge_array[y_start+1:(y_end+1), x_start+1:x_end] =\
                                                         False
                else:
                    fill_edge_array[y_start+1:(y_end+1), x_start+1:(x_end+1)] =\
                                                         False

    outputArr = basic_grid*fill_edge_array

    mpimg.imsave(outputfile, outputArr, cmap='Greys', format='png',\
                 dpi=dpi)


if __name__ == "__main__":
    inputfile = 'C:\Users\Michael\Desktop\patterns\Back.png'
    outputfile = 'C:\Users\Michael\Desktop\patterns\knitBack.png'
    center = (10, 10)
    pix_per_grid_shape = (25, 30)
    dpi = 150
    gridify(inputfile, outputfile, center, pix_per_grid_shape,\
            dpi)

