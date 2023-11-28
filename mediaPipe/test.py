import numpy as np

def rad_to_deg(rad):
    deg = rad*180/np.pi
    return deg

a = [2,7]
b = [3,3]
c = [4,6]

#x is represented by an index of 0
#y is represented by an index of 1
#G is point on base to the right of B

radian_cbg = np.arctan2(c[1]-b[1], c[0]-b[0])
#radian_bc = np.arctan2(b[1]-c[1], b[0]-c[0])
radian_abg = np.arctan2(a[1]-b[1], a[0]-b[0])

print("radians_cbg: ", round(radian_cbg, 2))
print("degrees_cbg: ", round(rad_to_deg(radian_cbg), 2))

#print("radians_bc: ", radian_bc)
#print("degrees_bc: ", rad_to_deg(radian_bc))

print("radians_abg: ", round(radian_abg, 2))
print("degrees_abg: ", round(rad_to_deg(radian_abg), 2))

radian_abc = radian_abg-radian_cbg

print("Angle abgc radians: ", round(radian_abc, 2))
print("Angle abgc degrees: ", round(np.abs(rad_to_deg(radian_abc)), 2))
