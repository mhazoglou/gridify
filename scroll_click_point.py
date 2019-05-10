import Tkinter
from PIL import Image, ImageTk

class scroll_click_point(Tkinter.Tk, Tkinter.Canvas):
    
    def __init__(self, canvas_width, canvas_height, filename):
        self.master = Tkinter.Tk.__init__(self)

        img = Image.open(filename)
        photo = ImageTk.PhotoImage(img)
        
        self.img = photo #Tkinter.PhotoImage(image=photo)
        if canvas_width > self.img.width():
            self.canvas_width = self.img.width()
        else:
            self.canvas_width = canvas_width
        if canvas_height > self.img.height():
            self.canvas_height = self.img.height()
        else:
            self.canvas_height = canvas_height
        
        self.canvas = Tkinter.Canvas(self,
                        width=self.canvas_width,
                        height=self.canvas_height)
        self.canvas.grid()
        self.canvas.bind('<Button-1>', self.return_point)
        self.canvas.bind('<ButtonRelease-1>', self.click_drag_anchor)
        self.canvas.bind('<Double-Button-1>',  self.double_click_center) 
        
        self.anchor_point = (0, 0)
        self.canvas.create_image(self.anchor_point, anchor="nw", image=self.img)
        self.center = None
    
    def double_click_center(self, event):
        self.center = (-self.anchor_point[0]\
                       + event.x, -self.anchor_point[1] + event.y)
        
    def return_point(self, event):
        self.start_point = (event.x, event.y)
    
    def click_drag_anchor(self, event):
        x_i, y_i = self.start_point
        x_f, y_f = (event.x, event.y)
        img_height = self.img.height()
        img_width = self.img.width()
        canvas_height = self.canvas_height
        canvas_width = self.canvas_width
        dh = img_height - canvas_height
        dw = img_width - canvas_width
        x_anchor = self.anchor_point[0] + x_f-x_i
        y_anchor = self.anchor_point[1] + y_f-y_i
        if x_anchor > 0:
            x_anchor = 0
        elif x_anchor < -dw+2:
            x_anchor = -dw+2
        
        if y_anchor > 0:
            y_anchor = 0
        elif y_anchor < -dh+2:
            y_anchor = -dh+2
        self.anchor_point = (x_anchor, y_anchor)
        self.canvas.create_image(self.anchor_point, anchor="nw", image=self.img)
