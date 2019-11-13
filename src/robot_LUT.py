import numpy as np

throwing_LUT = {3.0: "d:230", 2.1: "d:190", 1.67: "d:180", 1.0: "d:170"}
distances_LUT = np.array([1 ,  1.2, 1.25, 1.3, 1.35, 1.4, 1.7, 1.8,  1.92, 2.3, 2.4, 2.55, 2.7, 2.8, 3.1, 3.2])
speeds_LUT =    np.array([170, 174, 175, 176 ,178, 178,  183, 185,  187,  191, 196, 199, 202, 205, 209, 220])

def get_thrower_speed(distance):
    best_match = speeds_LUT[np.argmin(np.absolute(distances_LUT-distance))]
    return best_match



"""
distances_LUT = np.array([1  , 1.25, 1.5, 1.6, 1.7, 1.9, 2.16, 3.0, 3.3, 3.6])
speeds_LUT =    np.array([170, 170 , 180, 182, 182, 190, 200 , 210, 220, 230])
"""

#speeds_LUT = [170, 175, 180, 185, 190, 210, 220, 230]


"""

270 - 2.8
250 - 2.67
240 - 2.6
230 - 2.4
220 - 2.35
210 - 2.25
205 - 2.1
200 - 2.0
195 - 1.88
190 - 1.7
185 - 1.45
180 - 1.12
175 - 0.88
170 - 0.62
165 - 0.42



"""

