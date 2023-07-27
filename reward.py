def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels = params['all_wheels_on_track']
    speed = params['speed']
    progress = params['progress']
    is_offtrack = params['is_offtrack']
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
   
    # doubleed the speed rewards. i think car can go faster, but lets see if it can make the corners 
    if all_wheels:
        if speed >= 3:
            reward = reward + 2
        elif speed > 2 and speed < 3:
            reward = reward + 1
        elif speed > 1 and speed < 2:
            reward = reward + 0.5
        else:
            reward = reward + 0.1
    else:
        reward = reward - 1  # slighlt negate , but not a lot 
    
    if is_offtrack:
        reward = 1e-3  # penalize heavily for offtrack 
    else:
        reward = reward + 2  # we like being on track the most.

    # add progress to make car go further in track only in positive cases
    if reward > 0:
        return float(reward+progress)
    else:
        return float(reward)
