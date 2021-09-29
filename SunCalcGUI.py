# Written by Matthew DiMaggio
# Created 9/16/2021

from tkinter import *
from datetime import date
from datetime import datetime
import math
import time


def calculate_position(*args):
    for child in result_frame.winfo_children():
        child.destroy()

    lat = float(lat_entry.get())
    lng = float(lng_entry.get())

    timezone = float(utc_entry.get())  # Time difference from UTC time, accounting for daylight or standard time
    LT = float(hrs_entry.get()) + float(float(min_entry.get())/60)  # Local time, in 24 hour decimal format

    t = time.localtime()
    d0 = date(int(time.strftime("%Y", t)), 1, 1)
    d1 = date(int(time.strftime("%Y", t)), int(mth_entry.get()), int(day_entry.get()))
    daydelta = d1 - d0
    days = daydelta.days+1

    B = (360 / 365) * (days - 81)

    B_rad = math.radians(B)
    B_rad_two = math.radians(2 * B)

    dec = 23.45 * math.sin(B_rad)  # Declination
    EoT = (9.87 * math.sin(B_rad_two)) - (7.53 * math.cos(B_rad)) - (1.5 * math.sin(B_rad))  # Equation of Time
    LSTM = 15 * timezone  # Local Solar Time Meridian
    TC = 4 * (lng - LSTM) + EoT  # Time Correction
    LST = LT + (TC / 60)  # Local Solar Time
    HRA = 15 * (LST - 12)  # Hour Angle

    HRA_rad = math.radians(HRA)
    dec_rad = math.radians(dec)
    lat_rad = math.radians(lat)

    a0 = math.sin(dec_rad) * math.sin(lat_rad) + math.cos(dec_rad) * math.cos(lat_rad) * math.cos(HRA_rad)
    a = math.degrees(math.asin(a0))  # Solar Altitude

    a_rad = math.radians(a)

    Az0 = (math.sin(dec_rad) * math.cos(lat_rad) - math.cos(dec_rad) * math.sin(lat_rad) * math.cos(HRA_rad)) / (
        math.cos(a_rad))
    Az1 = math.degrees(math.acos(Az0))

    if (LST < 12) or (HRA < 0):
        Az = Az1  # Solar Azimuth
    else:
        Az = 360 - Az1  # Solar Azimuth

    riseset0 = ((-1*math.sin(lat_rad)*math.sin(dec_rad))/(math.cos(lat_rad)*math.cos(dec_rad)))
    sunrise = 12-(1/15)*math.degrees(math.acos(riseset0))-(TC/60)
    sunset = 12+(1/15)*math.degrees(math.acos(riseset0))-(TC/60)

    risehr = math.floor(sunrise)
    risemin = (round((sunrise - risehr)*60))
    if risemin == 60:
        risemin = 0
        risehr += 1
    rise0 = f'{risehr}:{risemin}'

    sethr = math.floor(sunset)
    setmin = (round((sunset - sethr) * 60))
    if setmin == 60:
        setmin = 0
        sethr += 1
    set0 = f'{sethr}:{setmin}'

    LSThr = math.floor(LST)
    LSTmin = (round((LST - LSThr) * 60))
    if LSTmin == 60:
        LSTmin = 0
        LSThr += 1
    LST0 = f'{LSThr}:{LSTmin}'

    sunrise_disp = datetime.strptime(rise0, "%H:%M")
    sunrise_disp = sunrise_disp.strftime("%I:%M %p")

    sunset_disp = datetime.strptime(str(set0), "%H:%M")
    sunset_disp = sunset_disp.strftime("%I:%M %p")

    print(set0)

    LST_disp = datetime.strptime(str(LST0), "%H:%M")
    LST_disp = LST_disp.strftime("%I:%M %p")

    riseHRA = math.radians(15 * ((sunrise + (TC / 60)) - 12))
    noonHRA = math.radians(15 * ((((sunrise+sunset)/2) + (TC / 60)) - 12))
    setHRA = math.radians(15 * ((sunset + (TC / 60)) - 12))

    risea0 = math.sin(dec_rad) * math.sin(lat_rad) + math.cos(dec_rad) * math.cos(lat_rad) * math.cos(riseHRA)
    risea = math.degrees(math.asin(risea0))

    riseAz0 = (math.sin(dec_rad) * math.cos(lat_rad) - math.cos(dec_rad) * math.sin(lat_rad) * math.cos(riseHRA)) / (
        math.cos(math.radians(risea)))
    riseAz = math.degrees(math.acos(riseAz0))

    noona0 = math.sin(dec_rad) * math.sin(lat_rad) + math.cos(dec_rad) * math.cos(lat_rad) * math.cos(noonHRA)
    noona = math.degrees(math.asin(noona0))

    noonAz0 = (math.sin(dec_rad) * math.cos(lat_rad) - math.cos(dec_rad) * math.sin(lat_rad) * math.cos(noonHRA)) / (
        math.cos(math.radians(noona)))
    noonAz = math.degrees(math.acos(round(noonAz0, 5)))

    seta0 = math.sin(dec_rad) * math.sin(lat_rad) + math.cos(dec_rad) * math.cos(lat_rad) * math.cos(setHRA)
    seta = math.degrees(math.asin(seta0))

    setAz0 = (math.sin(dec_rad) * math.cos(lat_rad) - math.cos(dec_rad) * math.sin(lat_rad) * math.cos(setHRA)) / (
        math.cos(math.radians(seta)))
    setAz = 360 - math.degrees(math.acos(setAz0))

    result_label_1 = Label(result_frame, justify=RIGHT, text=f'Declination: {round(dec, 2)}°\n'
                                            f'Local Solar Time Meridian: {round(LSTM, 2)}°\n'
                                            f'Local Solar Time: {LST_disp}\n'
                                            f'Sunrise: {sunrise_disp}\n'
                                                             f'Daylight: {round(sunset-sunrise, 2)} Hours')
    result_label_center = Label(result_frame, text=f'|\n|\n|\n|\n|\n|')
    result_label_2 = Label(result_frame, justify=LEFT, text=f'Equation of Time: {round(EoT, 2)} minutes\n'
                                            f'Time Correction: {round(TC, 2)} minutes\n'
                                            f'Hour Angle: {round(HRA, 2)}°\n'
                                            f'Sunset: {sunset_disp}\n'
                                                            f'Darkness: {round(24-(sunset-sunrise), 2)} Hours')
    sun_label_1 = Label(result_frame, justify=RIGHT, text=f'Solar Azimuth: {round(Az, 4)}°', font=('Helvetica', 10, 'bold'))
    sun_label_2 = Label(result_frame, justify=LEFT, text=f'Solar Altitude: {round(a, 4)}°', font=('Helvetica', 10, 'bold'))
    result_label_1.grid(row=0, column=0, sticky=E)
    result_label_center.grid(row=0, column=1, rowspan=2)
    result_label_2.grid(row=0, column=2, sticky=W)
    sun_label_1.grid(row=1, column=0, sticky=E)
    sun_label_2.grid(row=1, column=2, sticky=W)

    alt_offset = 250 * math.cos(math.radians(a))
    rise_offset = 250 * math.cos(math.radians(risea))
    noon_offset = 250 * math.cos(math.radians(noona))
    set_offset = 250 * math.cos(math.radians(seta))

    sunAzX = 300+(alt_offset*math.cos(math.radians(Az-90)))
    sunAzY = 300+(alt_offset*math.sin(math.radians(Az-90)))

    riseAzX = 300 + (rise_offset * math.cos(math.radians(riseAz - 90)))
    riseAzY = 300 + (rise_offset * math.sin(math.radians(riseAz - 90)))

    noonAzX = 300 + (noon_offset * math.cos(math.radians(noonAz - 90)))
    noonAzY = 300 + (noon_offset * math.sin(math.radians(noonAz - 90)))
    noonAzYInv = 300 + (noon_offset * math.sin(math.radians(noonAz + 90)))

    setAzX = 300 + (set_offset * math.cos(math.radians(setAz - 90)))
    setAzY = 300 + (set_offset * math.sin(math.radians(setAz - 90)))

    sunsphere_canvas.coords(sun_azumith, 300, 300, sunAzX, sunAzY)
    sunsphere_canvas.coords(sun, (sunAzX-10), (sunAzY-10), (sunAzX+10), (sunAzY+10))

    sunsphere_canvas.coords(sunrise_line, 300, 300, riseAzX, riseAzY)
    # sunsphere_canvas.coords(noon_line, 300, 300, noonAzX, noonAzY)
    sunsphere_canvas.coords(sunset_line, 300, 300, setAzX, setAzY)
    sunsphere_canvas.coords(sun_path, 50, noonAzYInv, 550, noonAzY)
    sunsphere_canvas.itemconfig(sun_path, start=riseAz+90, extent=setAz-riseAz, style=ARC)

    if a < 0:
        sunsphere_canvas.itemconfig(sun, fill="grey")
    else:
        sunsphere_canvas.itemconfig(sun, fill="yellow")


root = Tk()
root.title("Sun Calculator")
root.geometry("650x800")
root.resizable(0, 0)

# Title frame
title_frame = Frame(root)
title_frame.pack(side=TOP)

title_txt = Label(title_frame, text="Sun Position Calculator", font=('Helvetica', 10, 'bold'))
title_txt.pack(pady=10, padx=10)

# Entry Frame
entry_frame = Frame(root)
entry_frame.pack()

lat_label = Label(entry_frame, text="Latitude")
lng_label = Label(entry_frame, text="Longitude")
mth_label = Label(entry_frame, text="Month")
day_label = Label(entry_frame, text="Day")
yrs_label = Label(entry_frame, text="Year")
hrs_label = Label(entry_frame, text="Hour (24 Hr)")
min_label = Label(entry_frame, text="Minute")
utc_label = Label(entry_frame, text="Timezone UTC")

lat_var = StringVar()
lng_var = StringVar()
mth_var = StringVar()
day_var = StringVar()
yrs_var = StringVar()
hrs_var = StringVar()
min_var = StringVar()
utc_var = StringVar()

lat_entry = Entry(entry_frame, textvariable=lat_var)
lng_entry = Entry(entry_frame, textvariable=lng_var)
mth_entry = Entry(entry_frame, textvariable=mth_var)
day_entry = Entry(entry_frame, textvariable=day_var)
yrs_entry = Entry(entry_frame, textvariable=yrs_var)
hrs_entry = Entry(entry_frame, textvariable=hrs_var)
min_entry = Entry(entry_frame, textvariable=min_var)
utc_entry = Entry(entry_frame, textvariable=utc_var)

lat_label.grid(row=0, column=0, pady=1)
lng_label.grid(row=0, column=2, pady=1)
mth_label.grid(row=1, column=0, pady=1)
day_label.grid(row=1, column=2, pady=1)
yrs_label.grid(row=1, column=4, pady=1)
hrs_label.grid(row=2, column=0, pady=1)
min_label.grid(row=2, column=2, pady=1)
utc_label.grid(row=2, column=4, pady=1)

lat_entry.grid(row=0, column=1, pady=1)
lat_entry.focus()
lng_entry.grid(row=0, column=3, pady=1)
mth_entry.grid(row=1, column=1, pady=1)
day_entry.grid(row=1, column=3, pady=1)
yrs_entry.grid(row=1, column=5, pady=1)
hrs_entry.grid(row=2, column=1, pady=1)
min_entry.grid(row=2, column=3, pady=1)
utc_entry.grid(row=2, column=5, pady=1)

# Entry Default Values
t = time.localtime()
lat_entry.insert(0, "42.47461")
lng_entry.insert(0, "-83.24941")
mth_entry.insert(0, time.strftime("%m", t))
day_entry.insert(0, time.strftime("%d", t))
yrs_entry.insert(0, time.strftime("%Y", t))
hrs_entry.insert(0, time.strftime("%H", t))
min_entry.insert(0, time.strftime("%M", t))
utc_entry.insert(0, float(time.strftime("%z", t))/100)


# Sun Sphere Frame
sunsphere_frame = Frame(root)
sunsphere_frame.pack()
sunsphere_canvas = Canvas(sunsphere_frame, bg="white", height=600, width=600)
sunsphere_canvas.pack()

compass_x = sunsphere_canvas.create_line(300, 40, 300, 560, fill="blue")
compass_y = sunsphere_canvas.create_line(40, 300, 560, 300, fill="blue")
compass_N = sunsphere_canvas.create_text(300, 25, text="N", font=('Helvetica', 20))
compass_S = sunsphere_canvas.create_text(300, 575, text="S", font=('Helvetica', 20))
compass_E = sunsphere_canvas.create_text(575, 300, text="E", font=('Helvetica', 20))
compass_W = sunsphere_canvas.create_text(25, 300, text="W", font=('Helvetica', 20))

outer_circle = sunsphere_canvas.create_oval(50, 50, 550, 550)

sunrise_line = sunsphere_canvas.create_line(300, 300, 300, 300-250, fill="orange")
sunset_line = sunsphere_canvas.create_line(300, 300, 300, 300-250, fill="orange")

sun_path = sunsphere_canvas.create_arc(50, 50, 550, 550, start=86.686-90, extent=-273.523+90, outline="orange")
sun_azumith = sunsphere_canvas.create_line(300, 300, 300, 300-250)
sun = sunsphere_canvas.create_oval((300-10), ((300-250)-10), (300+10), ((300-250)+10), fill="yellow")


# Result Frame
result_frame = Frame(root)
result_frame.pack()

lat_var.trace_add("write", calculate_position)
lng_var.trace_add("write", calculate_position)
mth_var.trace_add("write", calculate_position)
day_var.trace_add("write", calculate_position)
yrs_var.trace_add("write", calculate_position)
hrs_var.trace_add("write", calculate_position)
min_var.trace_add("write", calculate_position)
utc_var.trace_add("write", calculate_position)

calculate_position()
mainloop()
