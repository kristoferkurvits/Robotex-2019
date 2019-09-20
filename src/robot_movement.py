import math

#rightwheel - middlewheel - left
#[0, 0, 0]

 
def calculate_linear_velocity(wheel_speed, wheel_angle, direction, middle_x_pixel=None, X=None, Y=None):
    if Y != None and Y != 0:
        direction = calculate_direction_angle(middle_x_pixel, X, Y, direction)
        wheel_linear_velocity = wheel_speed * math.cos(math.radians(direction - wheel_angle))
    else:
        wheel_linear_velocity = wheel_speed * math.cos(math.radians(direction - wheel_angle))


    return wheel_linear_velocity


def calculate_direction_angle(middle_x_pixel, X, Y, direction):
    direction = int(math.degrees(math.atan(middle_x_pixel - X) / Y) + direction)

    return direction




