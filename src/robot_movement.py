import math
import numpy as np
#rightwheel - middlewheel - left
#[0, 0, 0]

 
def calculate_linear_velocity(wheel_speed, wheel_angle, direction, middle_x_pixel=None, X=None, Y=None):
    if Y != None and Y != 0:
        direction = calculate_direction_angle(middle_x_pixel, X, Y, direction)
        wheel_linear_velocity = wheel_speed * math.cos(math.radians(direction - wheel_angle))
    else:
        wheel_linear_velocity = wheel_speed * math.cos(math.radians(direction - wheel_angle))

    return int(wheel_linear_velocity)

def calculate_direction_angle(middle_x_pixel, X, Y, direction):
    direction = int(math.degrees(math.atan((middle_x_pixel - X) / Y)) + direction)

    return direction

def move(processes_variables, ballInCenter, basket_distance, middle_x_pixel=None, ball_X=None, ball_Y=None, basket_X=None, basket_Y=None):
    wheel_speed = 24
    

    right_wheel_angle = 120
    middle_wheel_angle = 0
    left_wheel_angle = 240
    movement_direction_forward = 90
    circling_speed = 30

    """
    ball keskel -> korv näha -> vaatame palli korvi vahe/8, paneme kiiruseks ->
    -> kui centerX ja basketX < 30 ja centerX - ballX < 10, siis viskame

    """
# tagumine - liigub vasakule, + paremale
    
    ball_y_requirement = 320

    if ballInCenter:
        suggested_basket_speed = 30
        if basket_X != 0:
            basket_diff = middle_x_pixel - (basket_X)
            ball_diff = middle_x_pixel - ball_X
            suggested_basket_speed = min(basket_diff/4, 20)
            suggested_ball_speed = min(ball_diff/4, 20)
            """
            if suggested_ball_speed  > -3 and suggested_ball_speed < 0:
                suggested_ball_speed = -10

            if suggested_ball_speed  >= 0 and suggested_ball_speed < 3:
                suggested_ball_speed = 10

            if suggested_basket_speed  > -3 and suggested_basket_speed < 0:
                suggested_basket_speed = -10

            if suggested_basket_speed  >= 0 and suggested_basket_speed < 3:
                suggested_basket_speed = 10
            """
            if abs(basket_diff) < 15 and abs(ball_diff) < 15 and ball_Y > 380:
            #if (basket_diff >15 and basket_diff < 30) and abs(ball_diff) < 15 and ball_Y > ball_y_requirement:
                processes_variables[4] = 1
                with open("distances.txt", "a") as myfile:
                    myfile.write(str(basket_distance) + "\n")
                return
            elif abs(basket_diff) < 100 and abs(ball_diff) > 20:
                print(f"<<< BASKET: {suggested_ball_speed}")
                processes_variables[0] = int(calculate_linear_velocity(-suggested_ball_speed, right_wheel_angle, 180))
                processes_variables[1] = int(calculate_linear_velocity(suggested_ball_speed, middle_wheel_angle, 180))
                processes_variables[2] = int(calculate_linear_velocity(-suggested_ball_speed, left_wheel_angle, 180))
                return

                    
            
        if ball_Y > ball_y_requirement:
            circling_speed = min(suggested_basket_speed, circling_speed)
            processes_variables[0] = 0
            processes_variables[1] = -circling_speed
            processes_variables[2] = 0
        else:
            processes_variables[0] = int(calculate_linear_velocity(-wheel_speed, right_wheel_angle, movement_direction_forward, middle_x_pixel, ball_X, ball_Y))
            processes_variables[1] = int(calculate_linear_velocity(wheel_speed, middle_wheel_angle, movement_direction_forward, middle_x_pixel, ball_X, ball_Y))
            processes_variables[2] = int(calculate_linear_velocity(-wheel_speed, left_wheel_angle, movement_direction_forward, middle_x_pixel, ball_X, ball_Y))
    else:
        processes_variables[0] = wheel_speed
        processes_variables[1] = wheel_speed
        processes_variables[2] = wheel_speed

def rotateToBasket(ball_Y):
    pass


