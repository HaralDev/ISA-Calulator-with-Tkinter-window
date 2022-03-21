import math as math
from tkinter import *

### Window configuration 1
### Setting up the window with the tkinter module
window = Tk()
window.title("ISA calculator by Harald Luiks")
window.configure(background="white")

### Labelling before the text entry box
Label (window,text="The altitude in meters is: ",bg="white", fg="black", font="none 12 bold") .grid(row=1,column=0,sticky=W)

### Creating a text entry box for the altitude 
textentry = Entry (window,width=10,bg="white")
textentry.grid(row=2,column=0,sticky=W)

### return_atm_value function intitiates the calculation, this function is encapsulated in the submit button on line 80
def return_atm_value():
    entered_text = textentry.get()                                  # Collect text from entry box
    output.delete(0.0,END)
    alt = float(entered_text)
    
    if alt > 86000:                                                 # Give error if given altitude is higher than 86km
        output.insert(END,"No results above 86 km")
    else:      
        #======================================================
        # Constant, ISA SL values and some lists that we'll use
        r_gas= 287;                                                 # J/kgK        
        temp_sl = temp_bot = 273.15+15;                             # K at SL
        pres_sl = pres_bot = 101325;                                # Pa at SL
        grav0 = 9.80;                                               # m/s^2 at SL
        rho_sl = pres_sl / (r_gas*temp_sl);                         # Calculate rho at SL in kg/m3        
        alt_layer = (0, 11000, 20000, 32000, 47000, 51000, 71000);  # Temperature gradient thresholds
        t_grad = (-.0065, 0, .001, .0028, 0, -.0028, -.002);        # Temperature gradient in layers        
        l=0;                                                        # Arbitrary zero
       
        #=====================================================
        # Calculate Temp and Pressure for preceding atmosphere layer threshold
        while alt > alt_layer[l+1]:                            
            if t_grad[l] is not 0:                                  # Gradient layer threshold
                # Calculate the T and P of the top of last layer
                temp_top = temp_bot + (alt_layer[l+1]-alt_layer[l]) * t_grad[l]
                pres_bot = pres_bot * (temp_top/temp_bot)**(-(grav0)/(r_gas*t_grad[l]))
                temp_bot = temp_top                                 # Reset to bottom value
                
            else:                                                   # Isothermal layer threshold
                pres_bot = pres_bot * math.exp( (-1 * (alt_layer[l+1]-alt_layer[l]) * (grav0))/ (r_gas * temp_bot))               
            l = l + 1                                               # Update layer height for next iteration
        
        #=====================================================
        # Calculating Temperature, Pressure and Density at given altitude
 
        if t_grad[l] is not 0:                                      #Calculate the T and P for altitude in gradient layer
            temp_alt = temp_bot + (alt-alt_layer[l]) * t_grad[l]
            pres_alt = pres_bot*(temp_alt/temp_bot)**(-(grav0)/(r_gas*t_grad[l]))
        
        else:                                                       #Calculate the T and P for altitude in isothermal layer
            temp_alt = temp_bot
            pres_alt = pres_bot * math.exp( (-1 * (alt-alt_layer[l]) * (grav0))/ (r_gas * temp_alt))
        
        # Calculate rho and the ratios
        rho_alt = (pres_alt) / (r_gas * temp_alt)                   # Density calculation at given altitude
        p_ratio = (pres_alt / pres_sl)* 100                         # Pressure calculation at given altitude
        rh_ratio = (rho_alt / rho_sl)* 100                          # Density calculation at given altitude
               
        #=====================================================
        # Inserting results in textbox
        out_T = 'Temperature: {}K ({}C)'.format(round(temp_alt,2),round(temp_alt-273.15,1)) 
        out_P = 'Pressure: {}Pa ({}% SL)'.format(round(pres_alt,0),round(p_ratio,2))
        out_R = 'Density: {}kg/m3 ({}% SL)'.format(round(rho_alt,5),round(rh_ratio,2))
        out_list=[out_T,out_P,out_R]                                # List of the different results
               
        for i in range(3):                                          # For loop for appending output into result textbox
            output.insert(END,out_list[i])
            output.insert(END,'\n')
        
### Window configuration 2
# Submit button, this contains the return_atm_value function
Button (window,text = "Submit", width=8, command = return_atm_value) .grid(row=3, column=0, sticky=W)
 
# Result label
Label (window, text="Temperature, Pressure and Density at given altitude:",bg="white", fg="black", font="none 12 bold") .grid(row=4,column=0,sticky=W)

# Result field
output = Text (window,width=50,height=6,wrap = WORD, background ="white")
output.grid(row=5, column=0, columnspan=2, sticky=W)

# Exit button and window closure functions
def close_window():
    window.destroy()     
Button (window, text="Exit", width=14,command=close_window) .grid(row=6, column=0, sticky=W)

# Run window
window.mainloop() 
