from gridify import gridify
from scroll_click_point import scroll_click_point

def mancenter(inputfile, outputfile, pix_per_grid_shape, dpi,\
              threshold=0.5, width=700, height=600):
    """
	Allows for the manual selection of the center.
	
    Produces a window with the image of the pattern. Double clicking
    on the appropriate point selects it as the center. Scrolling on
    the image is done by clicking, dragging and releasing. Closing the
    window finalizes the choice of the center.
    
    inputfile - is a string containing the path and extension of
    the input png file

    outputfile - is a string containing the path and extension of
    the output png file

    pix_per_grid_shape - tuple specifying grid size in pixel e.g.
    (10, 20) for 10 pixels in width (horizontal/colums) and 20 in
    length (verticle/rows)

    dpi - dots per inch printing resolution

    threshold - value between 0 and 1 the criteria for making a
    patch in the pattern into a grid. The default is 0.5 meaning
    if half or more of then half of the pixels in the pattern are
    inside the patch it will become a grid block

    width - width of the window opened in pixels

    height = height of the window opened in pixels
    """

    center = None

    while center == None:
        mycanvas = scroll_click_point(width, height, inputfile)
        mycanvas.mainloop()
        center = mycanvas.center

    gridify(inputfile, outputfile, center, pix_per_grid_shape,\
            dpi, threshold=0.5)

if __name__ == "__main__":
    inputfile = 'C:\Users\Michael\Desktop\patterns\Back.png'
    outputfile = 'C:\Users\Michael\Desktop\patterns\knitBack.png'
    pix_per_grid_shape = (25, 30)
    dpi = 150
    mancenter(inputfile, outputfile, pix_per_grid_shape,\
            dpi)
