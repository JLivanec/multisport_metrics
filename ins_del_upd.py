from nicegui import ui
import mysql.connector
from nicegui.events import ValueChangeEventArguments
import random as rand
from datetime import date, datetime, timedelta
state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

def connect():
    global cnx
    global cursor
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password="JmanLivanec75898319!",
        port='3306',
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

        
    a_id = ''.join(["{}".format(rand.randint(0, 9)) for _ in range(0, 9)])

    athlete_data_minimal = {'AthleteID' : a_id, 'FirstName' : fn, 'LastName' : ln, 'Sex' : sex}
    add_athlete_minimal = ("INSERT INTO athlete"
                   "(AthleteID, FirstName, LastName, Sex)"
                   "VALUES (%(AthleteID)s, %(FirstName)s, %(LastName)s, %(Sex)s)")
    cursor.execute(add_athlete_minimal, athlete_data_minimal)

    cnx.commit()
    ui.notify("Athlete {0}, {1} has been added and assigned AthleteID {2}".format(ln, fn, a_id))
    #return to homepage
    return None

def insert_race(rn, city, state, type, rdate, s_dist, s_type, b_dist, b_elev, r_dist, r_elev):
    # check validity

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
    #return to homepage
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

#insert athlete
@ui.page('/ins_athlete_page')
def ins_athlete_page():
    with ui.row():
        ui.button('Connect', on_click=lambda:connect())
        ui.button('Disconnect', on_click=lambda:disconnect())
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

#################################################
    
#delete athlete
@ui.page('/del_athlete_page')
def del_athlete_page():
    if not is_connected():
        connect()
    ui.label('Choose Athlete to Delete')
    athletes = {}
    cursor.execute("SELECT AthleteID, FirstName, LastName FROM athlete ORDER BY LastName ASC")
    for (a_id, fn, ln) in cursor:
        athletes[a_id] = (ln + ", " + fn)

    
    del_athlete = ui.select(options= athletes, label='Choose Athlete', with_input=True)#.bind_value_to(globals(), 'result')
    
    ui.button('Delete', color='red', on_click = lambda: remove_athlete(del_athlete.value, athletes))

#################################################
    
#update athlete
@ui.page('/upd_athlete_page')
def upd_athlete_page():
    if not is_connected():
        connect()
    ui.label('Choose Athlete to Update')
    athletes = {}
    cursor.execute("SELECT AthleteID, FirstName, LastName FROM athlete ORDER BY LastName ASC")
    for (a_id, fn, ln) in cursor:
        athletes[a_id] = (ln + ", " + fn)
    
    upd_athlete = ui.select(options= athletes, label='Choose Athlete', with_input=True)#.bind_value_to(globals(), 'result')
    # here, we need to add an 'on_change' parameter calling a function to query the specific athlete based on id (the binding 
    # should always update result any time the selection is changed)
    
    #ui.button('Delete', color='red', on_click = lambda: remove_athlete(upd_athlete.value, athletes))
    #update = ui.button('Edit', color='green', on_click = None)
    #await update.clicked()
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

#################################################
#insert race with legs
@ui.page('/ins_race_page')
def ins_race_page():
    with ui.row():
        ui.button('Connect', on_click=lambda:connect())
        ui.button('Disconnect', on_click=lambda:disconnect())
    ui.label('Input Race Info')
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
            
    #only issue I see is that elevation and distance are varchar rather than float or int, didn't want to make
    #them number fields so left as text input
    
    ui.label('Swim Leg')
    swim_dist = ui.input(label='Swim Distance in Meters', placeholder='e.g. 1500', validation={'Input too long': lambda value: len(value) <= 10})
    # feel free to change defaults for open swim as well as the placeholder for all of these
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

#################################################
    
    
#delete race
@ui.page('/del_race_page')
def del_race_page():
    if not is_connected():
        connect()
    ui.label('Choose Race to Delete')
    races = {}
    rid = {}
    cursor.execute("SELECT Racename, RaceDate FROM race ORDER BY RaceDate DESC")
    for (rn, rd) in cursor:
        r_id = ''.join(["{}".format(rand.randint(0, 9)) for _ in range(0, 9)])
        races[r_id] = (rn + ", " + str(rd))
        rid[r_id] = [rn, rd]

    #result = 0
    del_race = ui.select(options= races, label='Choose Race', with_input=True)#.bind_value_to(globals(), 'result')
    
    ui.button('Delete', color='red', on_click = lambda: remove_race(rid[del_race.value][0], rid[del_race.value][1]))

#################################################
    
#update race with legs
@ui.page('/upd_race_page')
def upd_race_page():
    if not is_connected():
        connect()
    ui.label('Choose Race to Update')
    races = {}
    rid = {}
    cursor.execute("SELECT Racename, RaceDate FROM race ORDER BY RaceDate DESC")
    for (rn, rd) in cursor:
        r_id = ''.join(["{}".format(rand.randint(0, 9)) for _ in range(0, 9)])
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
    # feel free to change defaults for open swim as well as the placeholder for all of these
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

#################################################


ui.link('Insert Athlete', ins_athlete_page)
ui.link('Delete Athlete', del_athlete_page)
ui.link('Update Athlete', upd_athlete_page)

ui.link('Insert Race', ins_race_page)
ui.link('Delete Race', del_race_page)
ui.link('Update Race', upd_race_page)

ui.run()