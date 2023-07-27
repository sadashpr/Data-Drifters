def reward_function(params):

    class PARAMS:
        prev_all_wheels = None
        prev_steps = None

    # Read current input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels = params['all_wheels_on_track']
    speed = params['speed']
    progress = params['progress']
    is_offtrack = params['is_offtrack']
    steps = params['steps']

    # Reinitialize previous parameters if it is a new episode
    if PARAMS.prev_steps is None or steps < PARAMS.prev_steps:
        PARAMS.prev_all_wheels = None
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 5
    elif distance_from_center <= marker_2:
        reward = 3     # changed from 
    elif distance_from_center <= marker_3:
        reward = 1        # 
    else:
        reward = 1e-3  # likely crashed/ close to off track
   
    # doubled the speed rewards. i think car can go faster, but lets see if it can make the corners 
    if is_offtrack is False:              # changed all track to offtrack.. 
        if speed >= 3:
            reward = reward + 4
        elif speed > 2 and speed < 3:
            reward = reward + 3
        elif speed > 1 and speed < 2:
            reward = reward + 2
        else:
            reward = reward + 1
    else:
        reward = reward - 1  # slighlty negate , but not a lot 
    
    if is_offtrack:
        reward = 1e-3  # penalize heavily for offtrack 
    else:
        reward = reward + 2  # we like being on track the most.

    # new logic.. check if on track before and now 
    if PARAMS.prev_all_wheels is True and all_wheels is True:
        reward = reward + 2
    elif PARAMS.prev_all_wheels is False and all_wheels is True:
        reward = reward + 3
    elif PARAMS.prev_all_wheels is True and all_wheels is False:
        reward = reward - 1 
    else:
        reward = reward  

    # add rewards for every 10% progress.. this needs to be biggest reward of all to attract finishing.
    reward = reward + (int (progress/10))  
       
    # set params for next run 
    PARAMS.prev_all_wheels = all_wheels
    PARAMS.prev_steps = steps

    # add progress to make car go further in track only in positive cases
    return float(reward)
