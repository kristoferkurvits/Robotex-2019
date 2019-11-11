import math
import numpy as np
import time
#rightwheel - middlewheel - left
#[0, 0, 0]
right_wheel_angle = 120
middle_wheel_angle = 0
left_wheel_angle = 240
movement_direction_forward = 90

 
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

def rotateAroundSelf(processes_variables, circling_speed):
    processes_variables[0] = circling_speed
    processes_variables[1] = circling_speed
    processes_variables[2] = circling_speed

def omniToBall(processes_variables, movement_speed, middle_x_pixel, ball_X, ball_Y):
    processes_variables[0] = -calculate_linear_velocity(movement_speed, right_wheel_angle, movement_direction_forward, middle_x_pixel, ball_X, ball_Y)
    processes_variables[1] = calculate_linear_velocity(movement_speed, middle_wheel_angle, movement_direction_forward, middle_x_pixel, ball_X, ball_Y)
    processes_variables[2] = -calculate_linear_velocity(movement_speed, left_wheel_angle, movement_direction_forward, middle_x_pixel, ball_X, ball_Y)

def stopMoving(processes_variables):
    processes_variables[0] = 0
    processes_variables[1] = 0
    processes_variables[2] = 0

def rotateAroundBall(processes_variables, rotating_speed):
    processes_variables[0] = 0
    processes_variables[1] = rotating_speed
    processes_variables[2] = 0

def moveHorizontal(processes_variables, speed):
    processes_variables[0] = -calculate_linear_velocity(speed, right_wheel_angle, 180)
    processes_variables[1] = calculate_linear_velocity(speed, middle_wheel_angle, 180)
    processes_variables[2] = -calculate_linear_velocity(speed, left_wheel_angle, 180)

def moveVertical(processes_variables, speed):
    processes_variables[0] = -calculate_linear_velocity(speed, right_wheel_angle, 90)
    processes_variables[1] = calculate_linear_velocity(speed, middle_wheel_angle, 90)
    processes_variables[2] = -calculate_linear_velocity(speed, left_wheel_angle, 90)

def alignHorizontal(processes_variables, diff_from_center, P, min_speed, max_speed):
    X_speed = diff_from_center/P
    if X_speed <= 0:
        calculated_speed = -min(min_speed+abs(X_speed), max_speed)
        #calculated_speed = -forward_speed
    else:
        calculated_speed = min(min_speed+X_speed, max_speed)
        #calculated_speed = forward_speed
    moveHorizontal(processes_variables, calculated_speed)

def alignVertical(processes_variables, diff_from_center, P, min_speed, max_speed):
    X_speed = diff_from_center/P
    if X_speed <= 0:
        calculated_speed = -min(min_speed+abs(X_speed), max_speed)
        #calculated_speed = -forward_speed
    else:
        calculated_speed = min(min_speed+X_speed, max_speed)
        #calculated_speed = forward_speed
    moveVertical(processes_variables, calculated_speed)
    

def move(processes_variables, ballSeen, basket_distance, middle_x_pixel=None, ball_X=None, ball_Y=None, basket_X=None, basket_Y=None):
    


    # tagumine - liigub vasakule, + paremale
    ball_y_requirement = 330
    omni_forward_speed = 40
    forward_speed = 20
    circling_speed = 32
    rotation_speed = 10

    ball_dist_from_reqY = ball_y_requirement - ball_Y
    ball_dist_from_centerX = middle_x_pixel - ball_X

    basket_dist_from_centerX = middle_x_pixel - basket_X

    # kui näeme palli
    if ballSeen:
        # kui pall pole meile piisavalt lähedal
        if ball_dist_from_reqY > 90:
            Y_speed = ball_dist_from_reqY/2
            calculated_speed = min(6+Y_speed, omni_forward_speed)
            
            omniToBall(processes_variables, omni_forward_speed, middle_x_pixel, ball_X, ball_Y)

        elif ball_dist_from_reqY <= 90 and ball_dist_from_reqY > 10:

            
            alignVertical(processes_variables, ball_dist_from_reqY, 20, 8, forward_speed)

        elif abs(ball_dist_from_centerX) > 35:

            
            alignHorizontal(processes_variables, ball_dist_from_centerX, 20, 14, forward_speed)

        else:

            if abs(basket_dist_from_centerX) < 7:
                if abs(ball_dist_from_centerX) < 20:

                    stopMoving(processes_variables)
                    time.sleep(0.3)
                    processes_variables[4] = 1
                    return
                else:
                    
                    alignHorizontal(processes_variables, ball_dist_from_centerX, 20, 5, forward_speed)
            else:
                min_speed = 10
                X_speed = basket_dist_from_centerX/(320/(circling_speed-min_speed))
                if X_speed <= 0:
                    calculated_speed = min(min_speed+abs(X_speed), circling_speed)
                else:
                    calculated_speed = -(min(min_speed+X_speed, circling_speed))
                
                rotateAroundBall(processes_variables, calculated_speed)


    # kui palli ei näe, siis keerleme
    else:
        rotateAroundSelf(processes_variables, rotation_speed)












    """if ballInCenter: # KAS PALL ON NÄHA
        suggested_basket_speed = 30
        if basket_X != 0: # KAS KORVI ON
            basket_diff = middle_x_pixel - (basket_X)
            ball_diff = middle_x_pixel - ball_X
            suggested_basket_speed = min(basket_diff/6, np.sign(basket_diff)*20)
            suggested_ball_speed = min(ball_diff/6, np.sign(ball_diff)*20)

            if abs(basket_diff) < 15 and abs(ball_diff) < 25 and ball_Y > ball_y_requirement: # KAS KÕIK ON ALIGNED -> VISKAME
            #if (basket_diff >15 and basket_diff < 30) and abs(ball_diff) < 15 and ball_Y > ball_y_requirement:
                processes_variables[4] = 1
                return
            elif abs(basket_diff) < 100 and abs(ball_diff) > 20:

                               
                print(f"<<< BASKET: {suggested_ball_speed}")
                if ball_diff <= 0:
                    angle = 0
                else:
                    angle = 180
                processes_variables[0] = int(calculate_linear_velocity(-suggested_ball_speed, right_wheel_angle, angle))
                processes_variables[1] = int(calculate_linear_velocity(suggested_ball_speed, middle_wheel_angle, angle))
                processes_variables[2] = int(calculate_linear_velocity(-suggested_ball_speed, left_wheel_angle, angle))
                return

                    
            
        if ball_Y > ball_y_requirement: # KAS PALL ON NORMIS Y KOHAS
            circling_speed = min(suggested_basket_speed, circling_speed)
            processes_variables[0] = 0
            processes_variables[1] = -circling_speed
            processes_variables[2] = 0
        else:# SÕIDAME PALLI POOLE
            processes_variables[0] = int(calculate_linear_velocity(-wheel_speed, right_wheel_angle, movement_direction_forward, middle_x_pixel, ball_X, ball_Y))
            processes_variables[1] = int(calculate_linear_velocity(wheel_speed, middle_wheel_angle, movement_direction_forward, middle_x_pixel, ball_X, ball_Y))
            processes_variables[2] = int(calculate_linear_velocity(-wheel_speed, left_wheel_angle, movement_direction_forward, middle_x_pixel, ball_X, ball_Y))
    else: # KEERUTAME
        turning_speed = 10
        processes_variables[0] = turning_speed
        processes_variables[1] = turning_speed
        processes_variables[2] = turning_speed"""

def rotateToBasket(ball_Y):
    pass


