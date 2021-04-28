# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 00:39:52 2019

@author: hrmb

Please use the following link to learn more about GUI programming in python
using tkinter module. 
https://www.geeksforgeeks.org/python-gui-tkinter/

"""

import tkinter
from random import randint

class Emergence:
    
    def __init__(self, gridsize = 10, gridtype = 0):
        """ initialize the emergence grid
        """
        if gridsize > 10:
            print("grid size is reduced to the max size 10")
            self.gridsize = 10
        else:
            self.gridsize = gridsize # number of grid points in each dimension
        
        self.dotsize = 10 # the diameter for each dot
        self.xspace = 40 # the space between two adjacent dots
        self.yspace = self.xspace
        self.numberofcolors = 2 # could be more than 2
        self.TOTALGRIDRATIO = 0.8
        self.gridcolors = [[0] * self.gridsize] * self.gridsize # to save the colors for each point
        self.coords = [[(0,0)] * self.gridsize] * self.gridsize # to save coordinates of grid dots
        self.gridwidth = 0
        self.canvaswidth = 0 
		
		# at this point, we only have one example 10x10 grid
		# if user requires an example grid with size smaller than 10,
		# we will use the top left subsquare of the 10x10 example
        if gridtype == 0 : # use the example grid
            examplegridcolors = [[0, 1, 0, 0, 0, 1, 0, 0, 1, 1], #row 1
                     [1, 1, 0 ,0, 0, 1, 0, 0, 0, 1],  #row 2
                     [0, 0, 0, 1, 1, 0, 1, 0, 0, 1],  #row 3
                     [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],  #row 4
                     [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],  #row 5
                     [0, 0, 1, 0, 0, 1, 1, 0, 0, 1],  #row 6
                     [0, 1, 1, 0, 0, 0, 1, 1, 0, 1],  #row 7
                     [0, 0, 0, 1, 0, 1, 1, 0, 0, 1],
                     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 0, 1, 1, 0, 1, 1]]
					 
            self.gridcolors = examplegridcolors	 
			
        else:
		# initialize the grid using random numbers
            for i in range(self.gridsize):
                for j in range(self.gridsize):
                    self.gridcolors[i][j] = randint(0, self.numberofcolors - 1)
					
		# initialize the GUI window here. 
		# create the main window
        self.mainwindow = tkinter.Tk()
        # initialize the canvas to None. 
        self.canvas = None
       
	# use this function for debugging purposes   
    def printGrid(self):
        """ prints the gridcolors in text
        """
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                print(self.gridcolors[i][j] + "\t" , end="")
            print()
    
    # this function make the GUI window 
    def showindow(self):
        self.mainwindow.title("Emergence Grid")
        self.mainwindow.geometry("500x500") # default size of the window
        self.mainwindow.resizable(0, 0)
        self.mainwindow.bind('<Button-1>', self.onMouseClick) # bind the onMouseClick to the left mouse click <Button-1>
        # make the application ready to run. mainloop() is an infinite loop used to run the application, wait for an event to occur and process the event till the window is not closed.
        self.mainwindow.mainloop()
    
    def computeGridLayout(self):
        """ The computeGridLayout method computes the coordinates of the dots
        """
        # compute width and height of the grid
        self.gridwidth = self.gridsize * (self.dotsize + self.xspace)
        self.canvaswidth = self.gridwidth / self.TOTALGRIDRATIO 
        # create canvas
        if self.canvas == None :
            self.canvas = tkinter.Canvas(self.mainwindow, height = self.canvaswidth, width = self.canvaswidth)
        else:
            self.canvas.delete("all") # clear the canvas

        self.canvas.pack() 
        
    def drawGrid(self):
        """ draw the grid dots on canvas
        """
        r = self.dotsize //2
        topLeftCorner_x = (self.canvaswidth - self.gridwidth) //2 # make the grid to be on center of canvas
        topLeftCorner_y = topLeftCorner_x
        
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                # compute the coordinates of grid
                x = topLeftCorner_x + j * self.xspace
                y = topLeftCorner_y + i * self.yspace
                
                if self.gridcolors[i][j] == 0 :
                    color = "blue"
                else:
                    color = "red"
                    
                self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color) # draw a circle
                
	
	# put your code here. 
    
    def in_range(self,r,c):
        """ checks the range of the grid and returns False if the neighbor
            element is outside grid range
        """
        #for all elements inside the grid, return True
        if r >= 0 and c >= 0 and r < (self.gridsize) and c < (self.gridsize):
            return True
        else: #else false
            return False
        
    def ncheck(self,row,col):    
        blue = 0 #blue count
        red = 0 #red count
        #go through every inner element
        #loop for the dots neighbor range        
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if row != r or col != c: #exclude the position of the dot
                    if self.in_range(r,c) == True: #when in range
                        
                        #to check the neighbors and count blue and red
                        if self.gridcolors[r][c] == 0:
                            blue += 1
                        else:
                            red += 1            
        #return blue or red or equal cases
        if blue > red:
            return 0
        elif red > blue:
            return 1
        elif red == blue:
            return 2
            
            
    def updateEmergenceGrid(self):
        """ The updateEmergenceGrid function updates grid based on emergence rules
        """
        #create a new grid with all zeros
        newgrid = [[0 for i in range(self.gridsize)] for i in range (self.gridsize)]
        #evaluate individual elements
        #check the neighbors by calling ncheck then sets new grid as required
        for r in range(self.gridsize):
            for c in range(self.gridsize):
                #1 means more reds
                if self.ncheck(r,c) == 1:
                    newgrid[r][c] = 1
                #0 means more blues
                elif self.ncheck(r,c) == 0:
                    newgrid[r][c] = 0
                #2 means equal, so no changes
                elif self.ncheck(r,c) == 2:
                    newgrid[r][c] = self.gridcolors[r][c]
        #change the main grid            
        self.gridcolors = newgrid
	
    def onMouseClick(self, event):
        """ The onMouseClick event handler will call everytime user clicks on main form.
        """
        # each time you click on the form, you need to recompute grid layout and draw it. 
        # please remove the following two lines when you develope your code.
        self.computeGridLayout()
        self.drawGrid()
        self.updateEmergenceGrid()
        
        

if __name__ == "__main__":
    
    e = Emergence(10,0)
    e.showindow()

	
