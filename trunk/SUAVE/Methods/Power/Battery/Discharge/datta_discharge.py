# datta_discharge.py
# 
# Created:  ### ####, M. Vegh
# Modified: Feb 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np

# ----------------------------------------------------------------------
#  Datta Discharge
# ----------------------------------------------------------------------

def datta_discharge(battery,numerics): 
    """models discharge losses based on an empirical correlation
       Based on method taken from Datta and Johnson: 
       "Requirements for a Hydrogen Powered All-Electric Manned Helicopter"""""
    
    Ibat  = battery.inputs.current
    pbat  = battery.inputs.power_in
    Rbat  = battery.resistance
    I     = numerics.time.integrate
    D     = numerics.time.differentiate
    
    # Maximum energy
    max_energy = battery.max_energy
    
    #state of charge of the battery
    x = np.divide(battery.current_energy,battery.max_energy)

    # C rate
    C = np.abs(3600.*pbat/battery.max_energy)
    
    # Empirical value for discharge
    x[x<-35.] = -35. # Fix x so it doesn't warn
    
    f = 1-np.exp(-20.*x)-np.exp(-20.*(1.-x))
    
    f[f<0.0] = 0.0 # Negative f's don't make sense
    f = np.reshape(f, np.shape(C))
    
    # Model discharge characteristics based on changing resistance
    R          = Rbat*(1.+np.multiply(C,f)) #have to transpose to prevent large matrices
    R[R==Rbat] = 0.  #when battery isn't being called
    
    # Calculate resistive losses
    Ploss = (Ibat**2.)*R
    
    # Power going into the battery accounting for resistance losses
    P = pbat - Ploss*np.sign(pbat)
    
    # Possible Energy going into the battery:
    energy_unmodified = np.dot(I,P)
    
    # Available capacity
    capacity_available = max_energy - battery.current_energy[0]
   
    # How much energy the battery could be overcharged by
    delta           = energy_unmodified -capacity_available
    delta[delta<0.] = 0.
    
    # Power that shouldn't go in
    ddelta = np.dot(D,delta) 
    
    # Power actually going into the battery
    P[P>0.] = P[P>0.] - ddelta[P>0.]
    ebat = np.dot(I,P)
    ebat = np.reshape(ebat,np.shape(battery.current_energy)) #make sure it's consistent
    
    # Add this to the current state
    if np.isnan(ebat).any():
        ebat=np.ones_like(ebat)*np.max(ebat)
        if np.isnan(ebat.any()): #all nans; handle this instance
            ebat=np.zeros_like(ebat)

    battery.current_energy   = ebat + battery.current_energy[0]
    battery.resistive_losses = Ploss
    
    return
