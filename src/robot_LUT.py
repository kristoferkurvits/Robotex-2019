import numpy as np

throwing_LUT = {3.0: "d:230", 2.1: "d:190", 1.67: "d:180", 1.0: "d:170"}
distances_LUT = np.array([3.724 , 3.61,  3.5511, 3.458 , 3.192 , 3.1255, 2.9925, 2.793 , 2.66, 2.5004, 2.38, 2.261, 1.9285, 1.85, 1.78, 1.69, 1.58, 1.4896, 1.1704, 1.0, 0.8246, 0.65, 0.5586, 0.4])
speeds_LUT =    np.array([270, 260, 250, 245, 235, 220, 210, 208, 205, 199, 195, 192, 186, 183, 180, 180 ,178, 176, 175, 170, 170, 168, 165, 160])

def get_thrower_speed(distance):
    best_match = speeds_LUT[np.argmin(np.absolute(distances_LUT-distance))]
    return best_match
"""

distances_LUT = np.array([3.724 , 3.61,  3.5511, 3.458 , 3.192 , 3.1255, 2.9925, 2.793 , 2.66, 2.5004, 2.38, 2.261, 1.9285, 1.85, 1.78, 1.69, 1.58, 1.4896, 1.1704, 0.8246, 0.5586])
speeds_LUT =    np.array([270, 260, 250, 240, 230, 220, 210, 205, 202, 199, 195, 192, 186, 183, 180, 180 ,178, 175, 175, 170, 165])


2.836 - 205 jäi puudu


# 1.43 PEAKS OLEMA 177/178



otsime 2.8

2.9 - 2.8 = 0.1
3.0 - 2.8 = 0.2
"""
"""

1.59 184 üle normilt
1.57 184 üle

1.74 185 üle

1.38 180 üle normilt
1.35 180
1.66 184
1.86 186 üle
1.57 184
1.41 180
1.77 185 üle
0.75 170 üle






1.72 185 üle normilt
1.75 ka
1.81 185
1.69 185 üle
1.62 180 üle






distances_LUT = np.array([1  , 1.25, 1.5, 1.6, 1.7, 1.9, 2.16, 3.0, 3.3, 3.6])
speeds_LUT =    np.array([170, 170 , 180, 182, 182, 190, 200 , 210, 220, 230])
"""

#speeds_LUT = [170, 175, 180, 185, 190, 210, 220, 230]


"""
distances_LUT = np.array([2.8, 2.67, 2.6, 2.4, 2.35, 2.25, 2.1, 2.0, 1.88, 1.7, 1.45, 1.12, 0.88, 0.62, 0.42]) * 1.33
speeds_LUT =    np.array([270, 250, 240, 230, 220, 210, 207, 202, 198, 192, 187, 180, 175, 170, 165]) # 198 esimene

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
185 - 1.45xp
180 - 1.12
175 - 0.88
170 - 0.62
165 - 0.42












270 - 2.8
250 - 2.67
240 - 2.6 juurde törts
230 - 2.4
220 - 2.35 juurde vaja
210 - 2.25
205 - 2.1 207 veits maha
200 - 2.0 202 c
195 - 1.88 198 okei aga mööda
190 - 1.7 192 paras
185 - 1.45
180 - 1.12 184 suts palju, 180 suts palu
175 - 0.88 suts üle/ok
170 - 0.62
165 - 0.42









"""

