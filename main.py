"""This is just a simple authentication example.

Please see the `OAuth2 example at FastAPI <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>`_  or
use the great `Authlib package <https://docs.authlib.org/en/v0.13/client/starlette.html#using-fastapi>`_ to implement a classing real authentication system.
Here we just demonstrate the NiceGUI integration.
"""
import os
from typing import Optional
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from nicegui import Client, app, ui
import mysql.connector
import random as rand
import pandas as pd
from pace import *
import matplotlib.pyplot as plt
state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]


# in reality users passwords would obviously need to be hashed
users = {'user1':{'password': 'pass1', 'role': 'admin'}, 'user2':{'password': 'pass2', 'role': 'admin'}, 'user3':{'password': 'pass3', 'role': 'basic'}}

unrestricted_page_routes = {'/login', '/create-account'}

# Load environment variables from .env file
load_dotenv()

# Retrieve the secret key from an environment variable
secret_key = os.environ.get('CRYPT_SECRET_KEY')
cipher_suite = Fernet(secret_key)

class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')
        return await call_next(request)


app.add_middleware(AuthMiddleware)
def get_id(size):
    return ''.join(["{}".format(rand.randint(0, 9)) for _ in range(0, size)])

def connect():
    global cnx
    global cursor
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='multisport_metrics',
        auth_plugin='mysql_native_password'
    )
    if cnx.is_connected():
        ui.notify("Database Connection Successful")
        cursor = cnx.cursor()

    else:
        ui.notify("Database Connection Failed")

def disconnect():
    ui.notify("Database Disconnected")
    cnx.close()

def is_connected():
    if 'cnx' in globals():
        return cnx.is_connected()
    return False

def hms_to_s(h, m, s):
    s += m * 60
    s += h * 60 * 60
    return s

def sum_time(h, m, s):
    h = h or 0
    m = m or 0
    s = s or 0
    return hms_to_s(h, m, s)


def s_to_hms(s):
    h = s // 3600
    s = s % 3600
    m = s // 60
    s = s % 60
    return h, m, s

def get_timestring(time_total):
    h, m, s = s_to_hms(time_total)
    if not time_total:
        return ("--")
    if h and m:
        return ("{0}:{1}:{2}".format(int(h), str(int(m)).zfill(2), str(int(s)).zfill(2)))
    else:
       return ("{0}:{1}".format(str(int(m)).zfill(2), str(int(s)).zfill(2)))

def insert_athlete(fn, ln, grad, home, sex, dob):
    # check validity
    if fn == '':
        ui.notify("Missing Athlete First Name")
    if ln == '':
        ui.notify("Missing Athlete Last Name")
    if not is_connected():
        ui.notify("Database Not Connected")
    if fn == '' or ln == '' or not is_connected():
        return None

        
    a_id = get_id(10)

    if grad != None and grad != '':
        grad = round(grad)

    athlete_data = {'AthleteID' : a_id, 'FirstName' : fn, 'LastName' : ln, 'Sex' : sex, 'GradYear' : grad, 'Hometown' : home, 'DOB' : dob}
    add_athlete_minimal = ("INSERT INTO athlete"
                   "(AthleteID, FirstName, LastName, Sex)"
                   "VALUES (%(AthleteID)s, %(FirstName)s, %(LastName)s, %(Sex)s)")
    add_athlete_all = ("INSERT INTO athlete"
                   "(AthleteID, FirstName, LastName, Sex, GradYear, Hometown, DOB)"
                   "VALUES (%(AthleteID)s, %(FirstName)s, %(LastName)s, %(Sex)s, %(GradYear)s, %(Hometown)s, %(DOB)s)")
    add_athlete_hometown = ("INSERT INTO athlete"
                   "(AthleteID, FirstName, LastName, Sex, GradYear, Hometown)"
                   "VALUES (%(AthleteID)s, %(FirstName)s, %(LastName)s, %(Sex)s, %(GradYear)s, %(Hometown)s)")


    if athlete_data['DOB'] != '':
        cursor.execute(add_athlete_all, athlete_data)
    elif athlete_data['Hometown'] != '':
        cursor.execute(add_athlete_hometown, athlete_data)
    else:
        cursor.execute(add_athlete_minimal, athlete_data)

    cnx.commit()
    ui.notify("Athlete {0}, {1} has been added and assigned AthleteID {2}".format(ln, fn, a_id))
    return None

def insert_race(rn, city, state, type, rdate, s_dist, s_type, b_dist, b_elev, r_dist, r_elev):
    race_info = {'RaceName' : rn, 'City' : city, 'State' : state, 'Type' : type, 'RaceDate' : rdate}
    add_race = ("INSERT INTO race"
                   "(RaceName, City, State, Type, RaceDate)"
                   "VALUES (%(RaceName)s, %(City)s, %(State)s, %(Type)s, %(RaceDate)s)")
    cursor.execute(add_race, race_info)

    swim_info = {'RaceName' : rn, 'RaceDate' : rdate, 'LegName' : 'swim', 'Distance' : s_dist, 'Elevation' : s_type}
    bike_info = {'RaceName' : rn, 'RaceDate' : rdate, 'LegName' : 'bike', 'Distance' : b_dist, 'Elevation' : b_elev}
    run_info = {'RaceName' : rn, 'RaceDate' : rdate, 'LegName' : 'run', 'Distance' : r_dist, 'Elevation' : r_elev}
    add_leg = ("INSERT INTO leg"
                "(RaceName, RaceDate, LegName, Distance, Elevation)"
                "VALUES (%(RaceName)s, %(RaceDate)s, %(LegName)s, %(Distance)s, %(Elevation)s)")

    cursor.execute(add_leg, swim_info)
    cursor.execute(add_leg, bike_info)
    cursor.execute(add_leg, run_info)
    cnx.commit()
    ui.notify("Race {0} Added".format(rn))
    return None

def update_race(rn, city, state, type, rdate, s_dist, s_type, b_dist, b_elev, r_dist, r_elev):
    leg_query = "UPDATE leg SET Distance = %s, Elevation = %s WHERE (RaceName = %s AND RaceDate = %s AND LegName = %s)"
    swim_params = (s_dist, s_type, rn, rdate, 'swim')
    bike_params = (b_dist, b_elev, rn, rdate, 'bike')
    run_params = (r_dist, r_elev, rn, rdate, 'run')
    cursor.execute(leg_query, swim_params)
    cursor.execute(leg_query, bike_params)
    cursor.execute(leg_query, run_params)

    race_query = "UPDATE race SET City = %s, State = %s, Type = %s WHERE (RaceName = %s AND RaceDate = %s)"
    race_params = (city, state, type, rn, rdate)
    cursor.execute(race_query, race_params)
    
    ui.notify("Updated Race {0}".format(rn))
    cnx.commit()
    return None

def remove_athlete(a_id, athletes):
    query = "DELETE FROM athlete WHERE (AthleteID = %s)"
    athlete_id = (a_id,)
    cursor.execute(query, athlete_id)
    ui.notify("Deleted Athlete " + athletes[a_id])
    cnx.commit()
    return None

def remove_race(rn, rdate):
    query = 'DELETE FROM race WHERE (RaceName = %s AND RaceDate = %s)'
    params = (rn, rdate)
    cursor.execute(query, params)
    ui.notify("Deleted race " + rn)
    cnx.commit()
    return None

def update_athlete(a_id, fn, ln, grad, home, sex, dob):
    query = "UPDATE athlete SET FirstName = %s, LastName = %s, Sex = %s, GradYear = %s, Hometown = %s  WHERE AthleteID = %s"
    params = (fn, ln, sex, round(grad), home, a_id)
    cursor.execute(query, params)
    ui.notify("Updated Athlete {0}, {1}".format(ln, fn))
    cnx.commit()
    return None

def get_athlete_info(a_id) :
        if a_id != '' and a_id != None:
            cursor.execute("SELECT * FROM athlete WHERE AthleteID = " + a_id)
            return list(cursor)
        
def race(sh, sm, ss, t1m, t1s, bh, bm, bs, t2m, t2s, rh, rm, rs, toth, totm, tots, a_id, rname, rdate):
    swim_t = sum_time(sh, sm, ss)
    t1_t = sum_time(0, t1m, t1s)
    bike_t = sum_time(bh, bm, bs)
    t2_t = sum_time(0, t2m, t2s)
    run_t = sum_time(rh, rm, rs)
    total_t = sum_time(toth, totm, tots)

    record_leg = ("INSERT INTO legresults"
               "(AthleteID, RaceName, RaceDate, LegName, Time)"
               "VALUES (%s, %s, %s, %s, %s)")
    record_total = ("INSERT INTO raceresults"
               "(AthleteID, RaceName, RaceDate, TimeTotal)"
               "VALUES (%s, %s, %s, %s)")
    record_trans = ("INSERT INTO transitionresults"
               "(AthleteID, RaceName, RaceDate, TName, Time)"
               "VALUES (%s, %s, %s, %s, %s)")
    
    cursor.execute(record_leg, (a_id, rname, rdate, 'swim', swim_t))
    cursor.execute(record_leg, (a_id, rname, rdate, 'bike', bike_t))
    cursor.execute(record_leg, (a_id, rname, rdate, 'run', run_t))

    cursor.execute(record_total, (a_id, rname, rdate, total_t))

    cursor.execute(record_trans, (a_id, rname, rdate, 'T1', t1_t))
    cursor.execute(record_trans, (a_id, rname, rdate, 'T2', t2_t))
    ui.notify("Submission Successful")
    cnx.commit()
    return None

def remove_race_results(rname, rdate, a_id):
    rm_r_res = 'DELETE FROM raceresults WHERE (RaceName = %s AND RaceDate = %s AND AthleteID = %s)'
    rm_l_res = 'DELETE FROM legresults WHERE (RaceName = %s AND RaceDate = %s AND AthleteID = %s AND LegName = %s)'
    rm_t_res = 'DELETE FROM transitionresults WHERE (RaceName = %s AND RaceDate = %s AND AthleteID = %s AND TName = %s)'
    cursor.execute(rm_r_res, (rname, rdate, a_id))
    cursor.execute(rm_l_res, (rname, rdate, a_id, 'swim'))
    cursor.execute(rm_l_res, (rname, rdate, a_id, 'bike'))
    cursor.execute(rm_l_res, (rname, rdate, a_id, 'run'))
    cursor.execute(rm_t_res, (rname, rdate, a_id, 'T1'))
    cursor.execute(rm_t_res, (rname, rdate, a_id, 'T2'))
    ui.notify("Deleted Athlete {0}'s Results for Race {1}".format(a_id, rname))
    cnx.commit()
    return None

'''
@ui.page('/')
def main_page() -> None:
    with ui.column().classes('absolute-center items-center'):
        ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
        ui.label(f'Your role is {app.storage.user["role"]}!').classes('text-2xl')
        ui.button(on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/login')), icon='logout') \
            .props('outline round')
'''

def add_common_header():
    with ui.header().classes('flex justify-between items-center p-4 bg-blue-500 text-white'):
        ui.label('Multisport Metrics').classes('text-xl')
        if app.storage.user.get('authenticated', False):
            ui.label(f'Welcome, {app.storage.user["username"]}!')
            ui.button(icon= 'logout', text='Logout', on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/login'))).classes('btn btn-warning')
            ui.button('Account Details', on_click=lambda: ui.navigate.to('/account'))
            if app.storage.user['role'] == 'admin':
                with ui.button(text='Admin Tools'):
                    with ui.menu():
                        ui.menu_item('Create New User', on_click=lambda: ui.navigate.to('/create-account'))
                        ui.menu_item('Edit Users', on_click=lambda: ui.navigate.to('/edit-users'))

#insert athlete
@ui.page('/ins_athlete_page')
def ins_athlete_page():
    add_common_header()
    if app.storage.user['role'] == 'admin':
        if not is_connected():
            connect()
        ui.page_title('Insert Athlete')
        ui.label('Input Athlete Info')
        fn_input = ui.input(label='First Name', placeholder='e.g. John', validation={'Input too long': lambda value: len(value) <= 20})
        ln_input = ui.input(label='Last Name', placeholder='e.g. Smith', validation={'Input too long': lambda value: len(value) <= 20})
        grad_input = ui.number(label='Graduation Year', placeholder='e.g. 2024', min=1000, max=9999, 
                            precision=0, validation={'Please enter valid year': lambda value: value > 999 and value < 10000}).props('width=80')
        home_input = ui.input(label='Hometown', placeholder='e.g. Blacksburg, VA', validation={'Input too long': lambda value: len(value) <= 20})
        ui.label('Sex')
        sex_input = ui.toggle({'M': 'Male', 'F': 'Female', 'O': 'Other'}, value='M')
        with ui.input('Date of Birth') as date:
            with date.add_slot('append'):
                ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
            with ui.menu() as menu:
                ui.date().bind_value(date)

        ui.button('Submit', on_click = lambda: insert_athlete(fn_input.value, ln_input.value, grad_input.value, home_input.value, sex_input.value, date.value))
    else:
        ui.label('You are not authorized')

#delete athlete
@ui.page('/del_athlete_page')
def del_athlete_page():
    add_common_header()
    if app.storage.user['role'] == 'admin':
        if not is_connected():
            connect()
        ui.page_title('Delete Athlete')
        ui.label('Choose Athlete to Delete')
        athletes = {}
        cursor.execute("SELECT AthleteID, FirstName, LastName FROM athlete ORDER BY LastName ASC")
        for (a_id, fn, ln) in cursor:
            athletes[a_id] = (ln + ", " + fn)

        
        del_athlete = ui.select(options= athletes, label='Choose Athlete', with_input=True)#.bind_value_to(globals(), 'result')
        
        ui.button('Delete', color='red', on_click = lambda: remove_athlete(del_athlete.value, athletes))
    else:
        ui.label('You are not authorized')


#update athlete
@ui.page('/upd_athlete_page')
def upd_athlete_page():
    add_common_header()
    if app.storage.user['role'] == 'admin':
        if not is_connected():
            connect()
        ui.page_title('Update Athlete')
        ui.label('Choose Athlete to Update')
        athletes = {}
        cursor.execute("SELECT AthleteID, FirstName, LastName FROM athlete ORDER BY LastName ASC")
        for (a_id, fn, ln) in cursor:
            athletes[a_id] = (ln + ", " + fn)
        
        upd_athlete = ui.select(options= athletes, label='Choose Athlete', with_input=True, on_change=lambda : get_athlete_info(upd_athlete.value))#.bind_value_to(globals(), 'result')
        fn_input = ui.input(label='First Name', placeholder='e.g. John', validation={'Input too long': lambda value: len(value) <= 20})
        ln_input = ui.input(label='Last Name', placeholder='e.g. Smith', validation={'Input too long': lambda value: len(value) <= 20})
        grad_input = ui.number(label='Graduation Year', placeholder='e.g. 2024', min=1000, max=9999, 
                            precision=0, validation={'Please enter valid year': lambda value: value > 999 and value < 10000})
        home_input = ui.input(label='Hometown', placeholder='e.g. Blacksburg, VA', validation={'Input too long': lambda value: len(value) <= 20})
        ui.label('Sex')
        sex_input = ui.toggle({'M': 'Male', 'F': 'Female', 'O': 'Other'}, value='M')
        with ui.input('Date of Birth') as date:
            with date.add_slot('append'):
                ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
            with ui.menu() as menu:
                ui.date().bind_value(date)

        ui.button('Confirm Changes', color='green', on_click = lambda: update_athlete(upd_athlete.value, fn_input.value,
                                                                                ln_input.value, grad_input.value, home_input.value,
                                                                                sex_input.value, date.value))
    else:
        ui.label('You are not authorized')

#insert race with legs
@ui.page('/ins_race_page')
def ins_race_page():
    add_common_header()
    if app.storage.user['role'] == 'admin':
        if not is_connected():
            connect()
        ui.page_title('Insert Race')

        with ui.row():
            ui.link('Insert Athlete', ins_athlete_page)
            ui.link('Insert Race', ins_race_page)

        ui.label('Input Race Info')
        name_input = ui.input(label='Race Name', placeholder='e.g. Patriots Olympic', validation={'Input too long': lambda value: len(value) <= 90})
        city = ui.input(label='City', placeholder='e.g. Blacksburg', validation={'Input too long': lambda value: len(value) <= 20})
        state = ui.select(options= state_names, label='Choose State', with_input=True)
        ui.label('Race Type')
        r_type = ui.toggle(['sprint','olympic','half ironman','ironman','other'], value='olympic')
        
        with ui.input('Date of Race') as date:
            with date.add_slot('append'):
                ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
            with ui.menu() as menu:
                ui.date().bind_value(date)
        
        ui.label('Swim Leg')
        swim_dist = ui.input(label='Swim Distance in Meters', placeholder='e.g. 1500', validation={'Input too long': lambda value: len(value) <= 10})
        ui.label('Type of Swim')
        open_pool = ui.toggle({1: 'Open Water', 0: 'Pool'}, value=0)

        ui.label('Bike Leg')
        bike_dist = ui.input(label='Bike Distance in Miles', placeholder='e.g. 24.8', validation={'Input too long': lambda value: len(value) <= 10})
        ui.label('Bike Elevation')
        bike_elev = ui.input(label='Bike Elevation in Feet', validation={'Input too long': lambda value: len(value) <= 10}, value='0')

        ui.label('Run Leg')
        run_dist = ui.input(label='Run Distance', placeholder='e.g. 6.2', validation={'Input too long': lambda value: len(value) <= 10})
        ui.label('Run Elevation')
        run_elev = ui.input(label='Run Elevation in Feet', validation={'Input too long': lambda value: len(value) <= 10}, value='0')

        ui.button('Submit', on_click = lambda:insert_race(name_input.value, city.value, state.value, r_type.value, date.value, swim_dist.value, open_pool.value, bike_dist.value, bike_elev.value, run_dist.value, run_elev.value))
    else:
        ui.label('You are not authorized')

#delete race
@ui.page('/del_race_page')
def del_race_page():
    add_common_header()
    if app.storage.user['role'] == 'admin':
        if not is_connected():
            connect()
        ui.page_title('Delete Race')
        ui.label('Choose Race to Delete')
        races = {}
        rid = {}
        cursor.execute("SELECT Racename, RaceDate FROM race ORDER BY RaceDate DESC")
        for (rn, rd) in cursor:
            r_id = get_id(10)
            races[r_id] = (rn + ", " + str(rd))
            rid[r_id] = [rn, rd]

        #result = 0
        del_race = ui.select(options= races, label='Choose Race', with_input=True)
        
        ui.button('Delete', color='red', on_click = lambda: remove_race(rid[del_race.value][0], rid[del_race.value][1]))
    else:
        ui.label('You are not authorized')

#update race with legs
@ui.page('/upd_race_page')
def upd_race_page():
    add_common_header()
    if app.storage.user['role'] == 'admin':
        if not is_connected():
            connect()
        ui.page_title('Update Race')
        ui.label('Choose Race to Update')
        races = {}
        rid = {}
        cursor.execute("SELECT Racename, RaceDate FROM race ORDER BY RaceDate DESC")
        for (rn, rd) in cursor:
            r_id = get_id(10)
            races[r_id] = (rn + ", " + str(rd))
            rid[r_id] = [rn, rd]
        
        upd_race = ui.select(options= races, label='Choose Race', with_input=True)
        
        name_input = ui.input(label='Race Name', placeholder='e.g. Patriots Olympic', validation={'Input too long': lambda value: len(value) <= 30})
        city = ui.input(label='City', placeholder='e.g. Blacksburg', validation={'Input too long': lambda value: len(value) <= 20})
        state = ui.select(options= state_names, label='Choose State', with_input=True)
        ui.label('Race Type')
        r_type = ui.toggle(['sprint','olympic','half ironman','ironman','other'], value='olympic')
        
        with ui.input('Date of Race') as date:
            with date.add_slot('append'):
                ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
            with ui.menu() as menu:
                ui.date().bind_value(date)


        #### legs ####
                
        
        ui.label('Swim Leg')
        swim_dist = ui.input(label='Swim Distance in Meters', placeholder='e.g. 1500', validation={'Input too long': lambda value: len(value) <= 10})
        ui.label('Type of Swim')
        open_pool = ui.toggle({1: 'Open Water', 0: 'Pool'}, value=0)

        ui.label('Bike Leg')
        bike_dist = ui.input(label='Bike Distance in Miles', placeholder='e.g. 24.8', validation={'Input too long': lambda value: len(value) <= 10})
        ui.label('Bike Elevation')
        bike_elev = ui.input(label='Bike Elevation in Feet', validation={'Input too long': lambda value: len(value) <= 10}, value='0')

        ui.label('Run Leg')
        run_dist = ui.input(label='Run Distance', placeholder='e.g. 6.2', validation={'Input too long': lambda value: len(value) <= 10})
        ui.label('Run Elevation')
        run_elev = ui.input(label='Run Elevation in Feet', validation={'Input too long': lambda value: len(value) <= 10}, value='0')

        ui.button('Confirm Changes', color='green', on_click = lambda: update_race(rid[upd_race.value][0], city.value, state.value, r_type.value, rid[upd_race.value][1], swim_dist.value, open_pool.value, bike_dist.value, bike_elev.value, run_dist.value, run_elev.value))
    else:
        ui.label('You are not authorized')

#insert race results
@ui.page('/ins_results_page')
def ins_results_page():
    add_common_header()
    if app.storage.user['role'] == 'admin':
        if not is_connected():
            connect()
        ui.page_title('Insert Results')
        ui.label('Input Race Results')
        races = {}
        rid = {}
        cursor.execute("SELECT Racename, RaceDate FROM race ORDER BY RaceDate DESC")
        for (rn, rd) in cursor:
            r_id = get_id(10)
            races[r_id] = (rn + ", " + str(rd))
            rid[r_id] = [rn, rd]
        
        athletes = {}
        cursor.execute("SELECT AthleteID, FirstName, LastName FROM athlete ORDER BY LastName ASC")
        for (a_id, fn, ln) in cursor:
            athletes[a_id] = (ln + ", " + fn)
            
        race_choice = ui.select(options= races, label='Choose Race', with_input=True)
        athlete_choice = ui.select(options= athletes, label='Choose Athlete', with_input=True)

        #### legs ####
                
        ui.label('Swim Time')
        with ui.row():
            swim_h = ui.number(label='Hours')
            ui.label(':')
            swim_m = ui.number(label='Minutes')
            ui.label(':')
            swim_s = ui.number(label='Seconds')

        ui.label('T1')
        with ui.row():
            t1_m = ui.number(label = 'Minutes')
            ui.label(':')
            t1_s = ui.number(label = 'Seconds')

        ui.label('Bike Time')
        with ui.row():
            bike_h = ui.number(label='Hours')
            ui.label(':')
            bike_m = ui.number(label='Minutes')
            ui.label(':')
            bike_s = ui.number(label='Seconds')

        ui.label('T2')
        with ui.row():
            t2_m = ui.number(label = 'Minutes')
            ui.label(':')
            t2_s = ui.number(label = 'Seconds')

        ui.label('Run Time')
        with ui.row():
            run_h = ui.number(label='Hours')
            ui.label(':')
            run_m = ui.number(label='Minutes')
            ui.label(':')
            run_s = ui.number(label='Seconds')

        ui.label('Total Time')
        with ui.row():
            tot_h = ui.number(label='Hours')
            ui.label(':')
            tot_m = ui.number(label='Minutes')
            ui.label(':')
            tot_s = ui.number(label='Seconds')

        ui.button('Submit', on_click = lambda:race(swim_h.value, swim_m.value, swim_s.value,
                                                t1_m.value, t1_s.value,
                                                bike_h.value, bike_m.value, bike_s.value,
                                                t2_m.value, t2_s.value,
                                                run_h.value, run_m.value, run_s.value,
                                                tot_h.value, tot_m.value, tot_s.value,
                                                athlete_choice.value,
                                                rid[race_choice.value][0], rid[race_choice.value][1]))
    else:
        ui.label('You are not authorized')


#delete race
@ui.page('/del_results_page')
def del_results_page():
    add_common_header()
    if app.storage.user['role'] == 'admin':
        if not is_connected():
            connect()
        ui.page_title('Delete Results')
        ui.label('Choose Result to Delete')
        races = {}
        rid = {}
        cursor.execute("SELECT Racename, RaceDate FROM race ORDER BY RaceDate DESC")
        for (rn, rd) in cursor:
            r_id = get_id(10)
            races[r_id] = (rn + ", " + str(rd))
            rid[r_id] = [rn, rd]
        
        athletes = {}
        cursor.execute("SELECT AthleteID, FirstName, LastName FROM athlete ORDER BY LastName ASC")
        for (a_id, fn, ln) in cursor:
            athletes[a_id] = (ln + ", " + fn)
            
        race_choice = ui.select(options= races, label='Choose Race', with_input=True)
        athlete_choice = ui.select(options= athletes, label='Choose Athlete', with_input=True)

        ui.button('Delete', color='red', on_click = lambda: remove_race_results(rid[race_choice.value][0], rid[race_choice.value][1], athlete_choice.value))
    else:
        ui.label('You are not authorized')

@ui.page('/race_results')
def race_results_page():
    add_common_header()
    if not is_connected():
        connect()
    ui.page_title('View Results')
    ui.label('Choose Records to View')
    races = {}
    rid = {}
    cursor.execute("SELECT Racename, RaceDate FROM race ORDER BY RaceDate DESC")
    for (rn, rd) in cursor:
        r_id = get_id(10)
        races[r_id] = (rn + ", " + str(rd))
        rid[r_id] = [rn, rd]
    race_choice = ui.select(options= races, label='Choose Race', with_input=True)
    race_button = ui.button('Get Race Results')

    athletes = {}
    cursor.execute("SELECT AthleteID, FirstName, LastName FROM athlete ORDER BY LastName ASC")
    for (a_id, fn, ln) in cursor:
        athletes[a_id] = (ln + ", " + fn)
    #### this is the value for athlete ####
    athlete_choice = ui.select(options= athletes, label='Choose Athlete', with_input=True)
    athlete_button = ui.button('Get All Athlete Races')

    grid = ui.aggrid({
        'columnDefs': [],
        'rowData': []
    }).classes('min-h-screen')

    def filter_athlete():        
        athlete_query = '''WITH results AS(
                        SELECT
                            legresults.AthleteID,
                            legresults.RaceName,
                            legresults.RaceDate,
                            race.Type,
                            MAX(CASE WHEN legresults.LegName = 'swim' THEN legresults.Time ELSE 0 END) AS "swim_time",
                            MAX(CASE WHEN transitionresults.TName = 'T1' THEN transitionresults.Time ELSE 0 END) AS "t1_time",
                            MAX(CASE WHEN legresults.LegName = 'bike' THEN legresults.Time ELSE 0 END) AS "bike_time",
                            MAX(CASE WHEN transitionresults.TName = 'T2' THEN transitionresults.Time ELSE 0 END) AS "t2_time",
                            MAX(CASE WHEN legresults.LegName = 'run' THEN legresults.Time ELSE 0 END) AS "run_time",
                            MAX(raceresults.TimeTotal) AS "total_time"
                            FROM legresults
                            LEFT JOIN transitionresults
                            ON legresults.AthleteID = transitionresults.AthleteID AND
                                legresults.RaceName = transitionresults.RaceName AND
                                legresults.RaceDate = transitionresults.RaceDate
                            LEFT JOIN raceresults
                            ON legresults.AthleteID = raceresults.AthleteID AND
                                legresults.RaceName = raceresults.RaceName AND
                                legresults.RaceDate = raceresults.RaceDate
                            LEFT JOIN race
                            ON legresults.RaceName = race.RaceName AND
                                legresults.RaceDate = race.RaceDate
                            GROUP BY AthleteID, RaceName, RaceDate
                    )
                    SELECT 
                        athlete.LastName,
                        athlete.FirstName,
                        results.RaceName,
                        results.RaceDate,
                        results.Type,
                        results.swim_time,
                        results.t1_time,
                        results.bike_time,
                        results.t2_time,
                        results.run_time,
                        results.total_time
                    FROM athlete
                    LEFT JOIN results
                    ON athlete.AthleteID = results.AthleteID
                    WHERE results.RaceName IS NOT NULL AND athlete.AthleteID = (%s)
                    ORDER BY results.RaceDate DESC'''
        
        cursor.execute(athlete_query, (athlete_choice.value,))
        results = []
        for ln, fn, rn, rd, type, st, t1, bt, t2, rt, tt in cursor:
            result = {
            "Last Name": ln,
            "First Name": fn,
            "Race Name": rn,
            "Race Date": rd,
            "Type": type,
            "Swim Time": get_timestring(st),
            "T1 Time": get_timestring(t1),
            "Bike Time": get_timestring(bt),
            "T2 Time": get_timestring(t2),
            "Run Time": get_timestring(rt),
            "Total Time": get_timestring(tt)
            }
            results.append(result)

        grid.options['columnDefs'] = [
            {'headerName': 'Last Name', 'field': 'Last Name', 'filter': 'agTextColumnFilter'},
            {'headerName': 'First Name', 'field': 'First Name', 'filter': 'agTextColumnFilter'},
            {'headerName': 'Race Name', 'field': 'Race Name', 'filter': 'agTextColumnFilter'},
            {'headerName': 'Race Date', 'field': 'Race Date', 'filter': 'agDateColumnFilter'},
            {'headerName': 'Race Distance', 'field': 'Type', 'filter': 'agTextColumnFilter'},
            {'headerName': 'Swim Time', 'field': 'Swim Time', 'filter': 'agNumberColumnFilter'},
            {'headerName': 'T1 Time', 'field': 'T1 Time', 'filter': 'agNumberColumnFilter'},
            {'headerName': 'Bike Time', 'field': 'Bike Time', 'filter': 'agNumberColumnFilter'},
            {'headerName': 'T2 Time', 'field': 'T2 Time', 'filter': 'agNumberColumnFilter'},
            {'headerName': 'Run Time', 'field': 'Run Time', 'filter': 'agNumberColumnFilter'},
            {'headerName': 'Total Time', 'field': 'Total Time', 'filter': 'agNumberColumnFilter'}
        ]
        grid.options['rowData'] = results

        grid.update()
    
    athlete_button.on('click',filter_athlete)
    ui.run()


    def filter_race(): 
        race_query = ('''WITH results AS(
                        SELECT
                            legresults.AthleteID,
                            legresults.RaceName,
                            legresults.RaceDate,
                            MAX(CASE WHEN legresults.LegName = 'swim' THEN legresults.Time ELSE 0 END) AS "swim_time",
                            MAX(CASE WHEN transitionresults.TName = 'T1' THEN transitionresults.Time ELSE 0 END) AS "t1_time",
                            MAX(CASE WHEN legresults.LegName = 'bike' THEN legresults.Time ELSE 0 END) AS "bike_time",
                            MAX(CASE WHEN transitionresults.TName = 'T2' THEN transitionresults.Time ELSE 0 END) AS "t2_time",
                            MAX(CASE WHEN legresults.LegName = 'run' THEN legresults.Time ELSE 0 END) AS "run_time",
                            MAX(raceresults.TimeTotal) AS "total_time"
                            FROM legresults
                            LEFT JOIN transitionresults
                            ON legresults.AthleteID = transitionresults.AthleteID AND
                                legresults.RaceName = transitionresults.RaceName AND
                                legresults.RaceDate = transitionresults.RaceDate
                            LEFT JOIN raceresults
                            ON legresults.AthleteID = raceresults.AthleteID AND
                                legresults.RaceName = raceresults.RaceName AND
                                legresults.RaceDate = raceresults.RaceDate
                            GROUP BY AthleteID, RaceName, RaceDate
                    )
                    SELECT 
                        athlete.LastName,
                        athlete.FirstName,
                        results.RaceName,
                        results.RaceDate,
                        results.swim_time,
                        results.t1_time,
                        results.bike_time,
                        results.t2_time,
                        results.run_time,
                        results.total_time
                    FROM athlete
                    LEFT JOIN results
                    ON athlete.AthleteID = results.AthleteID
                    WHERE results.RaceName LIKE(%s) AND results.RaceDate = (%s)
                    ORDER BY results.total_time ASC''')
        race_params = (rid[race_choice.value][0], rid[race_choice.value][1])
        cursor.execute(race_query, race_params)
        results = []
        for ln, fn, rn, rd, st, t1, bt, t2, rt, tt in cursor:
            result = {
                "Last Name": ln,
                "First Name": fn,
                "Race Name": rn,
                "Race Date": rd,
                "Swim Time": get_timestring(st),
                "T1 Time": get_timestring(t1),
                "Bike Time": get_timestring(bt),
                "T2 Time": get_timestring(t2),
                "Run Time": get_timestring(rt),
                "Total Time": get_timestring(tt)
            }
            results.append(result)
        grid.options['columnDefs'] = [
            {'headerName': 'Last Name', 'field': 'Last Name', 'filter': 'agTextColumnFilter'},
            {'headerName': 'First Name', 'field': 'First Name', 'filter': 'agTextColumnFilter'},
            {'headerName': 'Race Name', 'field': 'Race Name', 'filter': 'agTextColumnFilter'},
            {'headerName': 'Race Date', 'field': 'Race Date', 'filter': 'agDateColumnFilter'},
            {'headerName': 'Swim Time', 'field': 'Swim Time', 'filter': 'agNumberColumnFilter'},
            {'headerName': 'T1 Time', 'field': 'T1 Time', 'filter': 'agNumberColumnFilter'},
            {'headerName': 'Bike Time', 'field': 'Bike Time', 'filter': 'agNumberColumnFilter'},
            {'headerName': 'T2 Time', 'field': 'T2 Time', 'filter': 'agNumberColumnFilter'},
            {'headerName': 'Run Time', 'field': 'Run Time', 'filter': 'agNumberColumnFilter'},
            {'headerName': 'Total Time', 'field': 'Total Time', 'filter': 'agNumberColumnFilter'}
        ]
        grid.options['rowData'] = results

        grid.update()
    race_button.on('click',filter_race)
    athlete_button.on('click',filter_athlete)

@ui.page('/all_results')
def all_results_page():
    add_common_header()
    if not is_connected():
        connect()
    ui.page_title('All Results')
    ui.label('All Results')

    cursor.execute('''WITH results AS(
                        SELECT
                            legresults.AthleteID,
                            legresults.RaceName,
                            legresults.RaceDate,
                            MAX(CASE WHEN legresults.LegName = 'swim' THEN legresults.Time ELSE 0 END) AS "swim_time",
                            MAX(CASE WHEN transitionresults.TName = 'T1' THEN transitionresults.Time ELSE 0 END) AS "t1_time",
                            MAX(CASE WHEN legresults.LegName = 'bike' THEN legresults.Time ELSE 0 END) AS "bike_time",
                            MAX(CASE WHEN transitionresults.TName = 'T2' THEN transitionresults.Time ELSE 0 END) AS "t2_time",
                            MAX(CASE WHEN legresults.LegName = 'run' THEN legresults.Time ELSE 0 END) AS "run_time",
                            MAX(raceresults.TimeTotal) AS "total_time"
                            FROM legresults
                            LEFT JOIN transitionresults
                            ON legresults.AthleteID = transitionresults.AthleteID AND
                                legresults.RaceName = transitionresults.RaceName AND
                                legresults.RaceDate = transitionresults.RaceDate
                            LEFT JOIN raceresults
                            ON legresults.AthleteID = raceresults.AthleteID AND
                                legresults.RaceName = raceresults.RaceName AND
                                legresults.RaceDate = raceresults.RaceDate
                            GROUP BY AthleteID, RaceName, RaceDate
                    )
                    SELECT 
                        athlete.LastName,
                        athlete.FirstName,
                        results.RaceName,
                        results.RaceDate,
                        results.swim_time,
                        results.t1_time,
                        results.bike_time,
                        results.t2_time,
                        results.run_time,
                        results.total_time
                    FROM athlete
                    LEFT JOIN results
                    ON athlete.AthleteID = results.AthleteID
                    WHERE results.RaceName IS NOT NULL
                    ORDER BY athlete.LastName ASC, athlete.FirstName ASC, results.RaceDate DESC''')
    results = []
    for ln, fn, rn, rd, st, t1, bt, t2, rt, tt in cursor:
        athlete = {
            "Last Name": ln,
            "First Name": fn,
            "Race Name": rn,
            "Race Date": rd,
            "Swim Time": get_timestring(st),
            "T1 Time": get_timestring(t1),
            "Bike Time": get_timestring(bt),
            "T2 Time": get_timestring(t2),
            "Run Time": get_timestring(rt),
            "Total Time": get_timestring(tt)
        }
        results.append(athlete)
    grid = ui.aggrid({
    'columnDefs': [
        {'headerName': 'Last Name', 'field': 'Last Name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
        {'headerName': 'First Name', 'field': 'First Name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
        {'headerName': 'Race Name', 'field': 'Race Name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
        {'headerName': 'Race Date', 'field': 'Race Date', 'filter': 'agDateColumnFilter', 'floatingFilter': True},
        {'headerName': 'Swim Time', 'field': 'Swim Time', 'filter': 'agNumberColumnFilter', 'floatingFilter': True},
        {'headerName': 'T1 Time', 'field': 'T1 Time', 'filter': 'agNumberColumnFilter', 'floatingFilter': True},
        {'headerName': 'Bike Time', 'field': 'Bike Time', 'filter': 'agNumberColumnFilter', 'floatingFilter': True},
        {'headerName': 'T2 Time', 'field': 'T2 Time', 'filter': 'agNumberColumnFilter', 'floatingFilter': True},
        {'headerName': 'Run Time', 'field': 'Run Time', 'filter': 'agNumberColumnFilter', 'floatingFilter': True},
        {'headerName': 'Total Time', 'field': 'Total Time', 'filter': 'agNumberColumnFilter', 'floatingFilter': True}
    ],
    'rowData': results
    }).classes('min-h-screen')

@ui.page('/records')
def records_page():
    add_common_header()
    if not is_connected():
        connect()
    ui.page_title('Records')
    cursor.execute('''
        WITH oly AS(
        SELECT
        a.LastName,
        a.FirstName,
        a.raceName,
        a.raceDate,
        a.Time,
        a.LegName,
        a.Sex,
        r.Type
        FROM all_legs as a
        LEFT JOIN race r
        ON a.RaceName = r.RaceName AND
        a.RaceDate = r.RaceDate
        WHERE Type LIKE("olympic"))
        SELECT
        oly.FirstName,
        oly.LastName,
        oly.Time,
        oly.Sex,
        oly.LegName,
        oly.RaceDate,
        oly.RaceName
        FROM oly
        JOIN (SELECT MIN(Time) AS time FROM oly WHERE Time != 0 GROUP BY Sex, LegName) min
            ON oly.Time = min.time
        ORDER BY Sex ASC, LegName ASC; ''')
    womens_records = []
    mens_records = []
    for fn, ln, time, sex, legname, rd, rn in cursor:
        record = {
            "Name": (fn + " " + ln),
            "Time" : get_timestring(time),
            "Sex" : sex,
            "Leg" : ("Olympic " + legname),
            "Race Date" : rd,
            "Race Name" : rn
        }
        if sex == "F":
            womens_records.append(record)
        else:
            mens_records.append(record)

    cursor.execute('''
        SELECT
        FirstName,
        LastName,
        total_time,
        Sex,
        Type,
        RaceDate,
        RaceName
        FROM aggregated_results
        JOIN (SELECT MIN(total_time) AS time FROM aggregated_results WHERE total_time != 0 AND Type LIKE("olympic") GROUP BY Sex) min
            ON total_time = min.time
        ORDER BY Sex ASC;
                   ''')
    overall_records = []
    for fn, ln, time, sex, ty, rd, rn in cursor:
        record = {
            "Name": (fn + " " + ln),
            "Time" : get_timestring(time),
            "Sex" : sex,
            "Race Date" : rd,
            "Race Name" : rn
        }
        overall_records.append(record)

    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab("Men's Individual")
        two = ui.tab("Women's Individual")
        thre = ui.tab('Overall')
    with ui.tab_panels(tabs, value=thre).classes('w-full'):
        with ui.tab_panel(one):
            with ui.card():
                ui.label("Men's Individual Records")
                columns = [
                    {'name': 'Leg', 'label': 'Leg', 'field': 'Leg', 'required': True},
                    {'name': 'Name', 'label': 'Name', 'field': 'Name', 'required': True, 'align': 'left'},
                    {'name': 'Time', 'label': 'Time', 'field':'Time', 'required':True},
                    {'name': 'Race Date', 'label': 'Date', 'field' : 'Race Date', 'required':True},
                    {'name': 'Race Name', 'label': 'Race', 'field' : 'Race Name', 'required':True}
                ]
                rows = mens_records
                ui.table(columns=columns, rows=rows, row_key='name')
        with ui.tab_panel(two):
            with ui.card():
                ui.label("Women's Individual Records")
                columns = [
                    {'name': 'Leg', 'label': 'Leg', 'field': 'Leg', 'required': True},
                    {'name': 'Name', 'label': 'Name', 'field': 'Name', 'required': True, 'align': 'left'},
                    {'name': 'Time', 'label': 'Time', 'field':'Time', 'required':True},
                    {'name': 'Race Date', 'label': 'Date', 'field' : 'Race Date', 'required':True},
                    {'name': 'Race Name', 'label': 'Race', 'field' : 'Race Name', 'required':True}

                ]
                rows = womens_records
                ui.table(columns=columns, rows=rows, row_key='name')
        with ui.tab_panel(thre):
            with ui.card():
                ui.label("Overall Records")
                columns = [
                    {'name': 'Name', 'label': 'Name', 'field': 'Name', 'required': True},
                    {'name': 'Time', 'label': 'Time', 'field': 'Time', 'required': True, 'align': 'left'},
                    {'name': 'Sex', 'label': 'Sex', 'field':'Sex', 'required':True},
                    {'name': 'Race Date', 'label': 'Date', 'field' : 'Race Date', 'required':True},
                    {'name': 'Race Name', 'label': 'Race', 'field' : 'Race Name', 'required':True}
                ]
                rows = overall_records
                ui.table(columns=columns, rows=rows, row_key='name')  
  

@ui.page('/stats')
def stats_page():
    add_common_header()
    if not is_connected():
        connect()
    ui.page_title('Records')
    ui.link('View Records', records_page)
    cursor.execute('SELECT * FROM aggregated_results;')
    lastnames = []
    firstnames = []
    aids = []
    sexs = []
    types = []
    rns = []
    rds = []
    sts = []
    t1s = []
    bts = []
    t2s = []
    rts = []
    tts = []
    for ln, fn, aid, sex, type, rn, rd, st, t1, bt, t2, rt, tt in cursor:
        lastnames.append(ln)
        firstnames.append(fn)
        aids.append(aid)
        sexs.append(sex)
        types.append(type)
        rns.append(rn)
        rds.append(rd)
        sts.append(st)
        t1s.append(t1)
        bts.append(bt)
        t2s.append(t2)
        rts.append(rt)
        tts.append(tt)

    data = {'First Name': firstnames,
            'Last Name': lastnames,
            'Athlete ID': aids,
            'Sex': sex,
            'Type': types,
            'Race Name': rns,
            'Race Date': rds,
            'Swim Time': sts,
            'T1 Time': t1s,
            'Bike Time': bts,
            'T2 Time': t2s,
            'Run Time': rts,
            'Total Time': tts}
    df = pd.DataFrame(data)
    sprints = df[df['Type'] == "sprint"]
    olys = df[df['Type'] == "olympic"]
    hims = df[df['Type'] == "half ironman"]

    swim_times = [time for time in df['Swim Time'] if time > 0 and time < 10000]
    swim_sprint = [time for time in sprints['Swim Time'] if time > 0 and time < 10000]
    swim_oly = [time for time in olys['Swim Time'] if time > 0 and time < 10000]
    swim_him = [time for time in hims['Swim Time'] if time > 0 and time < 10000]

    t1_times = [time for time in df['T1 Time'] if time > 0 and time < 1000]
    t1_sprint = [time for time in sprints['T1 Time'] if time > 0 and time < 1000]
    t1_oly = [time for time in olys['T1 Time'] if time > 0 and time < 1000]
    t1_him = [time for time in hims['T1 Time'] if time > 0 and time < 1000]

    bike_times = [time for time in df['Bike Time'] if time > 0 and time < 60000]
    bike_sprint = [time for time in sprints['Bike Time'] if time > 0 and time < 60000]
    bike_oly = [time for time in olys['Bike Time'] if time > 0 and time < 60000]
    bike_him = [time for time in hims['Bike Time'] if time > 0 and time < 60000]

    t2_times = [time for time in df['T2 Time'] if time > 0 and time < 1000]
    t2_sprint = [time for time in sprints['T2 Time'] if time > 0 and time < 1000]
    t2_oly = [time for time in olys['T2 Time'] if time > 0 and time < 1000]
    t2_him = [time for time in hims['T2 Time'] if time > 0 and time < 1000]

    run_times = [time for time in df['Run Time'] if time > 0 and time < 60000]
    run_sprint = [time for time in sprints['Run Time'] if time > 0 and time < 60000]
    run_oly = [time for time in olys['Run Time'] if time > 0 and time < 60000]
    run_him = [time for time in hims['Run Time'] if time > 0 and time < 60000]

    total_times = [time for time in df['Total Time'] if time > 0]
    sprint_times = [time for time in sprints['Total Time'] if time > 0]
    oly_times = [time for time in olys['Total Time'] if time > 0]
    run_times = [time for time in hims['Total Time'] if time > 0]


    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab("Overall")
        two = ui.tab("Sprint Distance")
        thre = ui.tab('Olympic Distance')
        fore = ui.tab('Half Ironman Distance')
    with ui.tab_panels(tabs, value=one).classes('w-full'):
        with ui.tab_panel(one):
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(swim_times, bins=20, color='skyblue', edgecolor='black')
                plt.title('Distribution of Swim Times')
                plt.xlabel('Swim Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(bike_times, bins=20, color='purple', edgecolor='black')
                plt.title('Distribution of Bike Times')
                plt.xlabel('Bike Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(run_times, bins=20, color='crimson', edgecolor='black')
                plt.title('Distribution of Run Times')
                plt.xlabel('Run Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(t1_times, bins=20, color='purple', edgecolor='black')
                plt.title('Distribution of T1 Times')
                plt.xlabel('T1 Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(t2_times, bins=20, color='lightgrey', edgecolor='black')
                plt.title('Distribution of T2 Times')
                plt.xlabel('T2 Time (seconds)')
                plt.grid(True)

        with ui.tab_panel(two):
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(swim_sprint, bins=20, color='skyblue', edgecolor='black')
                plt.title('Sprint Swim Times')
                plt.xlabel('Swim Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(bike_sprint, bins=20, color='purple', edgecolor='black')
                plt.title('Sprint Bike Times')
                plt.xlabel('Bike Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(run_sprint, bins=20, color='crimson', edgecolor='black')
                plt.title('Sprint Run Times')
                plt.xlabel('Run Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(t1_sprint, bins=20, color='purple', edgecolor='black')
                plt.title('Sprint T1 Times')
                plt.xlabel('T1 Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(t2_sprint, bins=20, color='lightgrey', edgecolor='black')
                plt.title('Sprint T2 Times')
                plt.xlabel('T2 Time (seconds)')
                plt.grid(True) 
        with ui.tab_panel(thre):
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(swim_oly, bins=20, color='skyblue', edgecolor='black')
                plt.title('Olympic Swim Times')
                plt.xlabel('Swim Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(bike_oly, bins=20, color='purple', edgecolor='black')
                plt.title('Olympic Bike Times')
                plt.xlabel('Bike Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(run_oly, bins=20, color='crimson', edgecolor='black')
                plt.title('Olympic Run Times')
                plt.xlabel('Run Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(t1_oly, bins=20, color='purple', edgecolor='black')
                plt.title('Olympic T1 Times')
                plt.xlabel('T1 Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(t2_oly, bins=20, color='lightgrey', edgecolor='black')
                plt.title('Olympic T2 Times')
                plt.xlabel('T2 Time (seconds)')
                plt.grid(True) 

        with ui.tab_panel(fore):
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(swim_him, bins=10, color='skyblue', edgecolor='black')
                plt.title('Half Ironman Swim Times')
                plt.xlabel('Swim Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(bike_him, bins=10, color='purple', edgecolor='black')
                plt.title('Half Ironman Bike Times')
                plt.xlabel('Bike Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(run_him, bins=10, color='crimson', edgecolor='black')
                plt.title('Half Ironman Run Times')
                plt.xlabel('Run Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(t1_him, bins=10, color='purple', edgecolor='black')
                plt.title('Half Ironman T1 Times')
                plt.xlabel('T1 Time (seconds)')
                plt.grid(True)
            with ui.pyplot(figsize=(10, 6)):
                plt.hist(t2_him, bins=10, color='lightgrey', edgecolor='black')
                plt.title('Half Ironman T2 Times')
                plt.xlabel('T2 Time (seconds)')
                plt.grid(True) 


@ui.page('/login')
def login() -> Optional[RedirectResponse]:
    add_common_header()
    if not is_connected():
        connect()
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        cursor.execute("SELECT password, role FROM users WHERE username = %s", (username.value.lower(),))
        user = cursor.fetchone()
        
        if user:
            stored_encrypted_pass = user[0]
            stored_decrypted_pass = cipher_suite.decrypt(stored_encrypted_pass).decode()
            if stored_decrypted_pass == password.value:

                app.storage.user.update({'username': username.value, 'authenticated': True, 'role' : user[1]})
                ui.navigate.to(app.storage.user.get('referrer_path', '/'))  # go back to where the user wanted to go
            else:
                ui.notify('Wrong username or password', color='negative')
        else:
            ui.notify('Wrong username or password', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.card().classes('absolute-center'):
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)
        ui.button('Create Account', on_click=lambda: ui.navigate.to('/create-account'))
    return None

@ui.page('/create-account')
def create_account() -> None:
    add_common_header()
    if not is_connected():
        connect()
    def add_user() -> None:
        # Check if all fields are filled
        if not (new_username.value and email.value and first_name.value and last_name.value and password.value):
            ui.notify('Please fill in all fields.', color='negative')
            return
        
        # Check if the username already exists
        cursor.execute("SELECT username FROM users WHERE username = %s", (new_username.value.lower(),))
        if cursor.fetchone():
            ui.notify('Username already exists!', color='negative')
            return

        # Insert new user if username is unique
        encrypt_password = cipher_suite.encrypt(password.value.encode()).decode()
        cursor.execute("INSERT INTO users (username, password, role, email, FirstName, LastName) VALUES (%s, %s, %s, %s, %s, %s)",
                       (new_username.value.lower(), encrypt_password, role.value if 'admin' in app.storage.user.get('role', '') else 'basic', email.value, first_name.value, last_name.value))
        cnx.commit()
        
        ui.notify('User added successfully', color='positive')
        ui.navigate.to(app.storage.user.get('referrer_path', '/'))

    with ui.card().classes('absolute-center'):
        ui.label('Create New Account')
        new_username = ui.input('Username')
        email = ui.input('Email')
        first_name = ui.input('First Name')
        last_name = ui.input('Last Name')
        password = ui.input('Password', password=True)
        if 'admin' in app.storage.user.get('role', ''):
            role = ui.select(label='Role', options=['basic', 'admin'], value = 'basic')
        else:
            role = ui.input(value='basic')
            role.visible = False  # Hidden and set to basic for non-admins
        ui.button('Create Account', on_click=add_user)

@ui.page('/edit-users')
def edit_users() -> None:

    add_common_header()
    if not is_connected():
        connect()

    def remove_user_dialogue(username):
        with ui.dialog() as dialog, ui.card():
            ui.label(f'Remove user {username}?')
            with ui.row():
                ui.button('Yes', on_click=lambda: (remove_user(username), dialog.close()))
                ui.button('No', on_click=lambda: (dialog.clear(), dialog.close()))
        dialog.open()
    def remove_user(username):
        ####### need to update page upon deletion#########
        print('deleting')
        cursor.execute("DELETE FROM users WHERE (username = %s)", (username,))
        cnx.commit()
        ui.update()
    cursor.execute("SELECT FirstName, LastName, username, email, role FROM users")
    
    cards = {}
    with ui.column() as col:
        for fn, ln, un, em, r in cursor.fetchall():
            print (un)
            with ui.card() as cards[un]:
                ui.label(f'Name: {ln}, {fn}').classes('h1')
                unlabel = ui.label(f'Username: {un}').classes('h2')
                ui.label(f'Email: {em}').classes('h2')
                ui.label(f'Role: {r}')
                ui.button(text= 'Delete User', color='red', icon='trash', on_click=lambda un = un: remove_user(un))
    #cursor.reset()



@ui.page('/')
def homepage():
    add_common_header()
    ui.page_title('Multisport Metrics')
    if app.storage.user.get('role', '') == 'admin':
        with ui.card():
            ui.label('Insert')
            ui.link('Insert Athlete', ins_athlete_page)
            ui.link('Insert Race', ins_race_page)
            ui.link('Insert Race Results', ins_results_page)
        with ui.card():
            ui.label('Update')
            ui.link('Update Athlete', upd_athlete_page)
            ui.link('Update Race', upd_race_page)
        with ui.card():
            ui.label('Delete')
            ui.link('Delete Athlete', del_athlete_page)
            ui.link('Delete Race', del_race_page)
            ui.link('Delete Race Results', del_results_page)
    with ui.card():
        ui.label('View Results')
        ui.link('View Race Results', race_results_page)
        ui.link('All Results', all_results_page)
        ui.link('Records', records_page)
        ui.link('Statistics', stats_page)

ui.run(title= 'Multisport Metrics', storage_secret='THIS_NEEDS_TO_BE_CHANGED')