#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  5 11:01:01 2018

@author: harald
"""

import math as math
from tkinter import *
import numpy as np
import git 

### Window
window = Tk()
window.title("ISA calculator by Harald Luiks")
window.configure(background="white")

### Label
Label (window,text="The altitude in meters is: ",bg="white", fg="black", font="none 12 bold") .grid(row=1,column=0,sticky=W)

### Altitude entry box
textentry = Entry (window,width=10,bg="white")
textentry.grid(row=2,column=0,sticky=W)

### Click function intitiates calculation for everything
def click():
    entered_text = textentry.get()    # collect text from text entry box
    output.delete(0.0,END)
    alt = float(entered_text)
    
    if alt > 86000: # Give error if given altitude is higher than 86km
        output.insert(END,"No results above 86 km")
    else:
       
    ####
    
      #Constant, ISA SL values and some lists we'll use
        # Physical constants
        r_gas= 287           # J/kgK
        
        # SL values
        temp_sl = 273.15+15              # K at SL
        pres_sl = 101325                 # Pa at SL
        grav0 = 9.80                     # m/s^2 at SL
        rho_sl = pres_sl/(r_gas*temp_sl)  #calculate rhoSL in kg/m3
                
        # Temp gradient list
        alt_layer = (0, 11000, 20000, 32000, 47000, 51000, 71000)
        t_grad = (-.0065, 0, .001, .0028, 0, -.0028, -.002)
        
        # Define which layers are thermodynamic and isothermal        
        l=0                     # Arbitrary zero
        l_iso = (1,4)           # Iso thermal layers
        l_grad = (0,2,3,5,6)    # Gradient layers
     
    ####   
        
        
        # Calculate which layer the altitude is in and the bottom values for each layer
        while alt >= alt_layer[l]:
            
            # Set SL values as bottom values of layer 
            if l == 0:           
                temp_bot = temp_sl
                pres_bot = pres_sl
                
            # Calculate values for the bottom of a layer succeeding a gradient layer
            elif l-1 in l_grad:     
                # Calculate the T and P of the top of last layer
                temp_top = temp_bot + (alt_layer[l]-alt_layer[l-1]) * t_grad[l-1]
                pres_top = pres_bot*(temp_top/temp_bot)**(-(grav0)/(r_gas*t_grad[l-1]))
                
                # Set these values as the bottom of the current layer
                temp_bot = temp_top
                pres_bot = pres_top
           
            # Calculate values for the bottom of a layer succeeding a isothermal layer 
            elif l-1 in l_iso:          
                temp_bot = temp_bot
                pres_top = pres_bot * math.exp( (-1 * (alt_layer[l]-alt_layer[l-1]) * (grav0))/ (r_gas * temp_bot))
                
                # Set calculated pressure as bottom of current layer
                pres_bot=pres_top
            
            # Update layer height, to check if the altitude is larger than the next atmosphere threshold
            l = l + 1  
        
        # The while loop stopped, so we now know that the altitude is in the l-1'th layer
        
        # Bring l back to the current layer:
        l=l-1
        
        #Calculate the T and P for altitude in gradient layer
        if l in l_grad:
            # Calculate the T and P of the top of last layer
            temp_alt = temp_bot + (alt-alt_layer[l]) * t_grad[l]
            pres_alt = pres_bot*(temp_alt/temp_bot)**(-(grav0)/(r_gas*t_grad[l]))
        
        elif l in l_iso:          
            temp_alt = temp_bot
            pres_alt = pres_bot * math.exp( (-1 * (alt-alt_layer[l]) * (grav0))/ (r_gas * temp_alt))
        
        # Calculate rho and the ratios
        rho_alt = (pres_alt) / (r_gas * temp_alt)
        p_ratio=(pres_alt / pres_sl)* 100
        rh_ratio=(rho_alt / rho_sl)* 100
        
        # Results
        temp = ("Temperature:", round(temp_alt,2),"K  (" ,round(temp_alt-273.15,1),"C )" )
        pres=("Pressure: ",round(pres_alt,0),"Pa  (",round(p_ratio,2)," % SL)")
        rho=("Density: ",round(rho_alt,5),"kg/m3  (",round(rh_ratio,2)," % SL)")
        
        textout=(temp,pres,rho)
        out=np.array(textout)
                      
        output.insert(END,out)

### Submit button
Button (window,text = "Submit", width=8, command=click) .grid(row=3, column=0, sticky=W)


### Result title
Label (window, text="Temperature, Pressure and Density at given altitude:",bg="white", fg="black", font="none 12 bold") .grid(row=4,column=0,sticky=W)


### Result field
output = Text (window,width=50,height=6,wrap = WORD, background ="white")
output.grid(row=5, column=0, columnspan=2, sticky=W)


### Exit button and functions
def close_window():
    window.destroy()  
   
Button (window, text="Exit", width=14,command=close_window) .grid(row=6, column=0, sticky=W)

### Open window
window.mainloop()
