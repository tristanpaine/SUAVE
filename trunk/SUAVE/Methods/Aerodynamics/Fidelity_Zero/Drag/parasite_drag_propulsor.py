# parasite_drag_propulsor.py
# 
# Created:  Dec 2013, SUAVE Team
# Modified: Jan 2016, E. Botero          

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
from SUAVE.Core import Data
from SUAVE.Core import Results
from compressible_turbulent_flat_plate import compressible_turbulent_flat_plate

# package imports
import numpy as np

# ----------------------------------------------------------------------
#   Parasite Drag Propulsor
# ----------------------------------------------------------------------

def parasite_drag_propulsor(state,settings,geometry):
    """ SUAVE.Methods.parasite_drag_propulsor(conditions,configuration,propulsor)
        computes the parasite drag associated with a propulsor 
        
        Inputs:

        Outputs:

        Assumptions:

        
    """

    # unpack inputs
    conditions    = state.conditions
    configuration = settings
    
    try:
        form_factor = configuration.propulsor_parasite_drag_form_factor
    except(AttributeError):
        form_factor = 2.3

    propulsor = geometry
    Sref      = propulsor.nacelle_diameter**2. / 4. * np.pi
    
    try:
        Swet = propulsor.areas.wetted
    except:
        propulsor.areas        = Data()
        propulsor.areas.wetted = 1.1 * propulsor.nacelle_diameter * np.pi * propulsor.engine_length
        Swet                   = propulsor.areas.wetted
    
    l_prop = propulsor.engine_length
    d_prop = propulsor.nacelle_diameter
    
    # conditions
    freestream = conditions.freestream
    Mc  = freestream.mach_number
    Tc  = freestream.temperature    
    re  = freestream.reynolds_number

    # reynolds number
    Re_prop = re*l_prop
    
    # skin friction coefficient
    cf_prop, k_comp, k_reyn = compressible_turbulent_flat_plate(Re_prop,Mc,Tc)
    
    # form factor for cylindrical bodies
    try: # Check if propulsor has an intake
        
        A_max = np.pi*(d_prop**2.)/4.
        A_exit = propulsor.A71
       
        A_inflow = propulsor.A0
        d_d = 1./((propulsor.engine_length + propulsor.nacelle_diameter) / np.sqrt((4./np.pi)*(A_max - (A_exit+A_inflow)/2.)))
      
        
        D = np.sqrt(1 - (1-Mc**2) * d_d**2)
        a        = 2. * (1-Mc**2) * (d_d**2) *(np.arctanh(D)-D) / (D**3)
        du_max_u = a / ( (2-a) * (1-Mc**2)**0.5 )
        k_prop    = (1 + form_factor*du_max_u)**2.
        
    except:
        # form factor according to Raymer equation (useful if there is a singularity in normal drag equation
        k_prop = 1 + 0.35 / (float(l_prop)/float(d_prop))
        
    
    # find the final result    
    propulsor_parasite_drag = k_prop * cf_prop * Swet / Sref
    
    # dump data to conditions
    propulsor_result = Results(
        wetted_area               = Swet    , 
        reference_area            = Sref    , 
        parasite_drag_coefficient = propulsor_parasite_drag ,
        skin_friction_coefficient = cf_prop ,
        compressibility_factor    = k_comp  ,
        reynolds_factor           = k_reyn  , 
        form_factor               = k_prop  ,
    )
    conditions.aerodynamics.drag_breakdown.parasite[propulsor.tag] = propulsor_result    
    
    return propulsor_parasite_drag