'''
        Proyecto IA

Points Engine

Creado por:

Juan Fernando De Leon Quezada   17822
Jose Gabriel Block Staackman    18935
'''

def railContact(customLabels, playersBall, frameDim, players_ball_previous_frame_info):
    '''Count how many times the player's 
    ball in turn touches the rails'''

    # Table Dimensions
    # x, y = poolTableDim

    # Frame Dimensions
    frame_height, frame_width = frameDim

    ball = None
    pool_table = None
    
    # Center of player's Ball
    center = None

    # Rails touched
    rail_contact_ctr = 0
    rails_touched_in_new_frame = []

    # Find Custom Label
    for label in customLabels:
        # If label is equals to player in turn
        if label['Name'] == playersBall:
            
            # Get Ball Info
            ball = label
        
        elif label['Name'] == 'Pool-Table':

            # Get Pool Table Info
            pool_table = label

    if ball != None:
        # Ball Dimensions in graph coordinates
        ball_top = ball['Geometry']['BoundingBox']['Top']
        ball_left = ball['Geometry']['BoundingBox']['Left']
        ball_width  = ball['Geometry']['BoundingBox']['Width']
        ball_height = ball['Geometry']['BoundingBox']['Height']

        # Ball Dimensions in pixels
        ball_top, ball_left, ball_width, ball_height = labelPositionInPX(ball_top, ball_left, ball_width, ball_height, frame_width, frame_height)

        # Calculate the center of the ball in pixels
        x = ball_left + (ball_width / 2)
        y = ball_top + (ball_height / 2)
        center = (x, y)

        # Pool Dimensions in graph coordinates
        # pool_table_top = pool_table['Geometry']['BoundingBox']['Top']
        # pool_table_left = pool_table['Geometry']['BoundingBox']['Left']
        # pool_table_width  = pool_table['Geometry']['BoundingBox']['Width']
        # pool_table_height = pool_table['Geometry']['BoundingBox']['Height']

        # Pool Dimensions in pixels
        # pool_table_top, pool_table_left, pool_table_width, pool_table_height = labelPositionInPX(pool_table_top, pool_table_left, pool_table_width, pool_table_height, frame_width, frame_height)
        pool_table_top = 250
        pool_table_left = 157
        pool_table_width  = 1408
        pool_table_height = 763

        # Calculate where the rails are
        top_rail = pool_table_left + 65
        bottom_rail = pool_table_left + pool_table_height - 65
        left_rail = pool_table_top + 65
        right_rail = pool_table_top + pool_table_width - 65

        rails_touched_in_prev_frame = players_ball_previous_frame_info[1]

        # Validate if the player's ball touched a rail
        if ((center[1] - ball_height) < top_rail < center[1]):
            # Touched the Top rail
            if "top_rail" not in rails_touched_in_prev_frame:
                rail_contact_ctr += 1
            
            rails_touched_in_new_frame.append("top_rail")

        if (center[1] < bottom_rail < (center[1] + ball_height)):
            # Touched the Bottom rail
            if "bottom_rail" not in rails_touched_in_prev_frame:
                rail_contact_ctr += 1
            
            rails_touched_in_new_frame.append("bottom_rail")
        
        if ((center[0] - ball_width) < left_rail < center[0]):
            # Touched the Left rail
            if "left_rail" not in rails_touched_in_prev_frame:
                rail_contact_ctr += 1
            
            rails_touched_in_new_frame.append("left_rail")
        
        if ((center[0]) < right_rail < (center[0] + ball_width)):
            # Touched the Right rail
            if "right_rail" not in rails_touched_in_prev_frame:
                rail_contact_ctr += 1
            
            rails_touched_in_new_frame.append("right_rail")
    
    return (center, rail_contact_ctr, rails_touched_in_new_frame)

# def validateRailTouch(players_ball_previous_frame, players_ball_new_frame):
#     '''Validate if it is a new rail touch'''
#     x_ball_previous_frame, y_ball_previous_frame, _ = players_ball_previous_frame
#     x_ball_new_frame, y_ball_new_frame = players_ball_new_frame
#     if (0 < abs(x_ball_previous_frame - x) < 20) and (0 < abs(y_ball_previous_frame - y) < 20):
#         # This means that we are counting twice
#         return

def ballsContact(customLabels, playersBall, frameDim):
    '''Detect Contact between balls, also returns where every ball is at'''
    
    # Table Dimensions
    # x, y = poolTableDim

    # Frame Dimensions
    frame_height, frame_width = frameDim

    player_ball = None
    opponent_ball = None
    red_ball = None
    pool_table = None

    # Find Custom Label
    for label in customLabels:
        # If label is equals to player in turn
        if label['Name'] == playersBall and player_ball == None:
            
            # Get Ball Info
            player_ball = label

        elif label['Name'] == 'Pool-Table' and pool_table == None:

            # Get Pool Table Info
            pool_table = label
        
        elif label['Name'] == 'Red-Ball' and red_ball == None:
            # Get red ball Info
            red_ball = label

        elif opponent_ball == None:
            opponent_ball = label

    if player_ball != None and red_ball != None and opponent_ball != None:
        # Player Ball Dimensions in graph coordinates
        player_ball_top = player_ball['Geometry']['BoundingBox']['Top']
        player_ball_left = player_ball['Geometry']['BoundingBox']['Left']
        player_ball_width  = player_ball['Geometry']['BoundingBox']['Width']
        player_ball_height = player_ball['Geometry']['BoundingBox']['Height']

        # Player Ball Dimensions in pixels
        player_ball_top, player_ball_left, player_ball_width, player_ball_height = labelPositionInPX(player_ball_top, player_ball_left, player_ball_width, player_ball_height, frame_width, frame_height)

        # Calculate the center of the player's ball in pixels
        player_x = player_ball_left + (player_ball_width / 2)
        player_y = player_ball_top + (player_ball_height / 2)
        player_center = (player_x, player_y)

        # print("Center of the Player's Ball: ", player_center)

        # Opponent Ball Dimensions in graph coordinates
        opponent_ball_top = opponent_ball['Geometry']['BoundingBox']['Top']
        opponent_ball_left = opponent_ball['Geometry']['BoundingBox']['Left']
        opponent_ball_width  = opponent_ball['Geometry']['BoundingBox']['Width']
        opponent_ball_height = opponent_ball['Geometry']['BoundingBox']['Height']

        # Opponent Ball Dimensions in pixels
        opponent_ball_top, opponent_ball_left, opponent_ball_width, opponent_ball_height = labelPositionInPX(opponent_ball_top, opponent_ball_left, opponent_ball_width, opponent_ball_height, frame_width, frame_height)

        # Calculate the center of the opponent's ball in pixels
        opponent_x = opponent_ball_left + (opponent_ball_width / 2)
        opponent_y = opponent_ball_top + (opponent_ball_height / 2)
        opponent_center = (opponent_x, opponent_y)

        # print("Center of the Opponent's Ball: ", opponent_center)

        # Red Ball Dimensions in graph coordinates
        red_ball_top = red_ball['Geometry']['BoundingBox']['Top']
        red_ball_left = red_ball['Geometry']['BoundingBox']['Left']
        red_ball_width  = red_ball['Geometry']['BoundingBox']['Width']
        red_ball_height = red_ball['Geometry']['BoundingBox']['Height']

        # Red Ball Dimensions in pixels
        red_ball_top, red_ball_left, red_ball_width, red_ball_height = labelPositionInPX(red_ball_top, red_ball_left, red_ball_width, red_ball_height, frame_width, frame_height)

        # Calculate the center of the red ball in pixels
        red_x = red_ball_left + (red_ball_width / 2)
        red_y = red_ball_top + (red_ball_height / 2)
        red_center = (red_x, red_y)

        # print("Center of the red's Ball: ", red_center)

        # Validate which ball touches which
        player_ball_bounding_box = (player_ball_top, player_ball_left, player_ball_width, player_ball_height)
        opponent_ball_bounding_box = (opponent_ball_top, opponent_ball_left, opponent_ball_width, opponent_ball_height)
        red_ball_bounding_box = (red_ball_top, red_ball_left, red_ball_width, red_ball_height)

        player_opponent_touch = touchBetweeBalls(player_ball_bounding_box, opponent_ball_bounding_box)
        player_red_touch = touchBetweeBalls(player_ball_bounding_box, red_ball_bounding_box)
        opponnent_red_touch = touchBetweeBalls(opponent_ball_bounding_box, red_ball_bounding_box)

        # print("player_opponent_touch", player_opponent_touch)
        # print("player_red_touch", player_red_touch)
        # print("opponnent_red_touch", opponnent_red_touch)

        if player_opponent_touch:
            return (player_center, opponent_center, red_center, ("player_opponent_touch", player_opponent_touch))
        elif player_red_touch:
            return (player_center, opponent_center, red_center, ("player_red_touch", player_red_touch))
        elif opponnent_red_touch:
            return (player_center, opponent_center, red_center, ("opponnent_red_touch", opponnent_red_touch))
        
        return (player_center, opponent_center, red_center, (None, None))

    return (None, None, None, (None, False))


def touchBetweeBalls(ball_1, ball_2):
    '''Calculate if two ball touches each other'''
    ball_1_top = ball_1[0]
    ball_1_left = ball_1[1]
    ball_1_width = ball_1[2]
    ball_1_height = ball_1[3]

    ball_2_top = ball_2[0]
    ball_2_left = ball_2[1]
    ball_2_width = ball_2[2]
    ball_2_height = ball_2[3]

    left_touch_1_2 = (ball_2_left <= ball_1_left + ball_1_width + 5 <= ball_2_left + ball_2_width) and (ball_2_top  <= ball_1_top + ball_1_height <= ball_2_top + ball_2_height)
    top_touch_1_2 = (ball_2_left <= ball_1_left + ball_1_width <= ball_2_left + ball_2_width + 5) and (ball_1_top <= ball_2_top <= ball_1_top + ball_1_height + 5)
    right_touch_1_2 = (ball_1_left <= ball_2_left + ball_2_width + 5 <= ball_1_left + ball_1_width) and (ball_1_top  <= ball_2_top + ball_2_height <= ball_1_top + ball_1_height)
    bottom_touch_1_2 = (ball_1_left <= ball_2_left + ball_2_width <= ball_1_left + ball_1_width + 5) and (ball_2_top <= ball_1_top <= ball_2_top + ball_2_height + 5)

    return left_touch_1_2 or top_touch_1_2 or right_touch_1_2 or bottom_touch_1_2
    

def labelPositionInPX(label_top, label_left, label_width, label_height, frame_width, frame_height):
    '''Calculate position in px'''
    return (label_top*frame_height, label_left*frame_width, label_width*frame_width, label_height*frame_height)
