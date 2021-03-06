import numpy as np
import SUAVE


# ----------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------

def unpack_body_angle(segment,state):

    # unpack unknowns
    theta      = state.unknowns.body_angle

    # apply unknowns
    state.conditions.frames.body.inertial_rotations[:,1] = theta[:,0]      


# ----------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------


def initialize_conditions(segment,state):
    
    # unpack
    throttle   = segment.throttle
    mach       = segment.mach  
    alt0       = segment.altitude_start 
    altf       = segment.altitude_end
    t_nondim   = state.numerics.dimensionless.control_points
    conditions = state.conditions  

    # check for initial altitude
    if alt0 is None:
        if not state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 * state.initials.conditions.frames.inertial.position_vector[-1,2]
        segment.altitude_start = alt0

    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0
    
    # pack conditions  
    conditions.propulsion.throttle[:,0] = throttle
    conditions.freestream.altitude[:,0]             =  alt[:,0] # positive altitude in this context
    SUAVE.Methods.Missions.Segments.Common.Aerodynamics.update_atmosphere(segment,state) # get density for airspeed
    density   = conditions.freestream.density[:,0]   
    atmos_data = segment.analyses.atmosphere.compute_values(alt,segment.temperature_deviation)
    speed_of_sound = atmos_data.speed_of_sound[:,0]
    segment.air_speed = speed_of_sound*mach
    air_speed = segment.air_speed
    conditions.frames.inertial.velocity_vector[:,0] = air_speed # start up value
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] # z points down
    
    
def update_velocity_vector_from_wind_angle(segment,state):
    
    # unpack
    conditions = state.conditions 
    v_mag      = segment.air_speed 
    theta      = state.unknowns.wind_angle[:,0][:,None]

    # process
    v_x =  v_mag * np.cos(theta[:,0])
    v_z = -v_mag * np.sin(theta[:,0]) # z points down

    # pack
    conditions.frames.inertial.velocity_vector[:,0] = v_x
    conditions.frames.inertial.velocity_vector[:,2] = v_z

    return conditions    
