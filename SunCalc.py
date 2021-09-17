# Written by Matthew DiMaggio - 9/16/2021

import math
import datetime

lat = 42.47490
lng = -83.24970

timezone = -4  # Time difference from UTC time, accounting for daylight or standard time
LT = 13.5  # Local time, in 24 hour decimal format
days = 258  # Days from Jan 1

B = (360 / 365) * (days - 81)

B_rad = math.radians(B)
B_rad_two = math.radians(2*B)

dec = 23.45*math.sin(B_rad)  # Declination
EoT = (9.87*math.sin(B_rad_two))-(7.53*math.cos(B_rad))-(1.5*math.sin(B_rad))  # Equation of Time
LSTM = 15 * timezone  # Local Solar Time Meridian
TC = 4*(lng-LSTM)+EoT  # Time Correction
LST = LT+(TC/60)  # Local Solar Time
HRA = 15*(LST-12)  # Hour Angle


HRA_rad = math.radians(HRA)
dec_rad = math.radians(dec)
lat_rad = math.radians(lat)

a0 = math.sin(dec_rad)*math.sin(lat_rad)+math.cos(dec_rad)*math.cos(lat_rad)*math.cos(HRA_rad)
a = math.degrees(math.asin(a0))  # Solar Altitude

a_rad = math.radians(a)

Az0 = (math.sin(dec_rad)*math.cos(lat_rad)-math.cos(dec_rad)*math.sin(lat_rad)*math.cos(HRA_rad))/(math.cos(a_rad))
Az = math.degrees(math.acos(Az0))  # Solar Azimuth


if LT > 12:
    LT_Hour = math.floor(LT) - 12
    AM_PM = "PM"
else:
    LT_Hour = math.floor(LT)
    AM_PM = "AM"

LT_Minute = round((LT-math.floor(LT))*60)

print(f'Latitude: {lat}\n'
      f'Longitude: {lng}\n'
      f'Timezone: UTC{timezone}\n'
      f'Local Time: {LT_Hour}:{LT_Minute} {AM_PM}\n\n'
      f'Declination: {dec}\n'
      f'Equation of Time: {EoT}\n'
      f'Local Solar Time Meridian: {LSTM}\n'
      f'Time Correction: {TC}\n'
      f'Local Solar Time: {LST}\n'
      f'Hour Angle: {HRA}\n\n'
      f'Solar Azimuth: {Az}°\n'
      f'Solar Altitude: {a}°')

