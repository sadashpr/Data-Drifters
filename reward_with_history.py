def reward_function(params):

    class PARAMS:
        prev_all_wheels = None
        prev_distance_from_center = None
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
        PARAMS.prev_distance_from_center = None
    
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
    ## car is still slow everywhere .. lets try to be faster , increased rewarsd for speed

    if speed >= 3:
        reward = reward + 5
    elif speed > 2:
        reward = reward + 4
    elif speed > 1:
        reward = reward + 3

    # just kill it if offtrack.. no point learning from here 
    if is_offtrack:
        reward = 1e-3  # penalize heavily for offtrack 
        return reward
    else:
        reward = reward + 2  # we like being on track 

    # new logic.. check if on track before and now 
    if PARAMS.prev_all_wheels is True and all_wheels is True:
        reward = reward + 2       # continuining on track
    elif PARAMS.prev_all_wheels is False and all_wheels is True:
        reward = reward + 3       # coming back on track 
    elif PARAMS.prev_all_wheels is True and all_wheels is False:
        reward = reward - 1       # tending to go off 

    if PARAMS.prev_distance_from_center is not None:
        if PARAMS.prev_distance_from_center < distance_from_center:
            reward = reward + 1  # heading to middle of track
        elif PARAMS.prev_distance_from_center == distance_from_center:
            reward = reward + 2  # staying where we are on track
        elif PARAMS.prev_distance_from_center > distance_from_center:
            reward = reward -1 # going away from center of track 


    # TODO:    #Penalize slowing down without good reason on straight portions
    #     if has_speed_dropped and not is_turn_upcoming:    use teams logic to calculate upcoming turn 


    # add rewards for every 12% progress.. this needs to be biggest reward of all to attract finishing.
    ## cahnging 10 to 12 to reduce the importance a bit.. 
    reward = reward + (int (progress/12))  
       
    # set params for next run 
    PARAMS.prev_all_wheels = all_wheels
    PARAMS.prev_distance_from_center = distance_from_center
    PARAMS.prev_steps = steps

    # add progress to make car go further in track only in positive cases
    return float(reward)
