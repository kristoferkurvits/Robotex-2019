import math

#rightwheel - middlewheel - left
#[0, 0, 0]

 
def calculate_linear_velocity(middle_x_pixel, X, Y, wheel_speed, wheel_angle, wheel_direction):  
    direction_angle = calculate_direction_angle(middle_x_pixel, X, Y)
    wheel_linear_velocity = wheel_speed * math.cos(direction_angle - wheel_angle)

    return wheel_linear_velocity

def calculate_x_speed(right_wheel, middle_wheel, left_wheel):
    robot_speed = (right_wheel + middle_wheel + left_wheel) / 3
    robot_speed_X = (right_wheel + middle_wheel) / 2

    return robot_speed_X
    
def calculate_y_speed(right_wheel, middle_wheel, left_wheel):
    robot_speed = (right_wheel + middle_wheel + left_wheel) / 3
    robot_speed_Y = (right_wheel + left_wheel) / 2

    return robot_speed_Y

def calculate_direction_angle(middle_x_pixel, X, Y):
    direction_angle = int(math.degrees(math.atan(middle_x_pixel - X) / Y) + 90)

    return direction_angle

