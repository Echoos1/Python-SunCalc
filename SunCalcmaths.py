import math

lat = 42.47490
lng = -83.24970

timezone = -4
LT = 13.5

days = 259

B = (360 / 365) * (days - 81)
print(B)

EoT = (9.87*math.sin(math.radians(2*B)))-(7.53*math.cos(math.radians(B)))-(1.5*math.sin(math.radians(B)))
print(EoT)

LSTM = 15 * timezone
print(LSTM)

TC = 4*(lng-LSTM)+EoT
print(TC)

LST = LT+(TC/60)
print(LST)

HRA = 15*(LST-12)
print(HRA)

dec = 23.45*math.sin(math.radians(B))
print(dec)

a0 = math.sin(math.radians(dec))*math.sin(math.radians(lat))+math.cos(math.radians(dec))*math.cos(math.radians(lat))*math.cos(math.radians(HRA))
print(a0)

a = math.degrees(math.asin(a0))
print(f'a = {a}')

Az0 = (math.sin(math.radians(dec))*math.cos(math.radians(lat))-math.cos(math.radians(dec))*math.sin(math.radians(lat))*math.cos(math.radians(HRA)))/(math.cos(math.radians(a)))
print(Az0)

Az = math.degrees(math.acos(Az0))
print(Az)
