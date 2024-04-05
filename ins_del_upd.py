from nicegui import ui
import mysql.connector
from nicegui.events import ValueChangeEventArguments
import random as rand
from datetime import date, datetime, timedelta
state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

def get_id(size):
    return ''.join(["{}".format(rand.randint(0, 9)) for _ in range(0, size)])

def connect():
    global cnx
    global cursor
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password="CSD@mysql-1872",
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

#insert athlete
@ui.page('/ins_athlete_page')
def ins_athlete_page():
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

#################################################
    
#delete athlete
@ui.page('/del_athlete_page')
def del_athlete_page():
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

#################################################
    
#update athlete
@ui.page('/upd_athlete_page')
def upd_athlete_page():
    if not is_connected():
        connect()
    ui.page_title('Update Athlete')
    ui.label('Choose Athlete to Update')
    athletes = {}
    cursor.execute("SELECT AthleteID, FirstName, LastName FROM athlete ORDER BY LastName ASC")
    for (a_id, fn, ln) in cursor:
        athletes[a_id] = (ln + ", " + fn)
    
    upd_athlete = ui.select(options= athletes, label='Choose Athlete', with_input=True, on_change=lambda : get_athlete_info(upd_athlete.value))#.bind_value_to(globals(), 'result')
    # here, we need to add an 'on_change' parameter calling a function to query the specific athlete based on id (the binding 
    # should always update result any time the selection is changed)
    
    #ui.button('Delete', color='red', on_click = lambda: remove_athlete(upd_athlete.value, athletes))
    #update = ui.button('Edit', color='green', on_click = None)

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
    del_race = ui.select(options= races, label='Choose Race', with_input=True)#.bind_value_to(globals(), 'result')
    
    ui.button('Delete', color='red', on_click = lambda: remove_race(rid[del_race.value][0], rid[del_race.value][1]))

#################################################
    
#update race with legs
@ui.page('/upd_race_page')
def upd_race_page():
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
    
#insert race results
@ui.page('/ins_results_page')
def ins_results_page():
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

#delete race
@ui.page('/del_results_page')
def del_results_page():
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

@ui.page('/race_results')
def race_results_page():
    if not is_connected():
        connect()
    ui.page_title('View Results')
    ui.label('Choose Race to View')
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

    ####possibly a way to specify an a specific race for a specific athlete####



    def filter_athlete():
        ####this is filtering by athlete, need query with more info#####
        #### change for loop and header names####
        
        race_query = ('Query for all results for the chosen athlete')
        race_params = (rid[race_choice.value][0], rid[race_choice.value][1])
        cursor.execute(race_query, race_params)
        results = []
        for '''race name and stats''' in cursor:
            result = {
                #race name and stats as keys
            }
            results.append(result)
        #rename headers for info we're getting about athlete's results
        grid.options['columnDefs'] = [
                                {'headerName': 'First Name', 'field': 'First Name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
                                {'headerName': 'Last Name', 'field': 'Last Name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
                                {'headerName': 'Total Time', 'field': 'Total Time', 'filter': 'agNumberColumnFilter', 'floatingFilter': True}
        ]
        grid.options['rowData'] = results

        grid.update()
    
    athlete_button.on('click',filter_athlete)
    #button = ui.button('Submit', on_click=filter_grid)

    ui.run()


    def filter_race():
        ####this is filtering by race, need query with more info#####
        #### change for loop and header names####
        
        race_query = ('SELECT athlete.FirstName, athlete.LastName, raceresults.TimeTotal FROM athlete LEFT JOIN raceresults ' + 
                      'ON raceresults.AthleteID = athlete.AthleteID WHERE raceresults.RaceName LIKE(%s) AND raceresults.RaceDate ' +
                      '= %s ORDER BY athlete.LastName ASC')
        race_params = (rid[race_choice.value][0], rid[race_choice.value][1])
        cursor.execute(race_query, race_params)
        results = []
        for fn, ln, tt in cursor:
            result = {
                "First Name": fn,
                "Last Name": ln,
                "Total Time": tt
            }
            results.append(result)
        grid.options['columnDefs'] = [
                                {'headerName': 'First Name', 'field': 'First Name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
                                {'headerName': 'Last Name', 'field': 'Last Name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
                                {'headerName': 'Total Time', 'field': 'Total Time', 'filter': 'agNumberColumnFilter', 'floatingFilter': True}
        ]
        grid.options['rowData'] = results

        grid.update()
    race_button.on('click',filter_race)
    athlete_button.on('click',filter_athlete)

    #button = ui.button('Submit', on_click=filter_grid)

    ui.run()


@ui.page('/all_results')
def all_results_page():
    
    if not is_connected():
        connect()
    ui.page_title('All Results')
    ui.label('All Results')
    races = {}
    rid = {}
    cursor.execute("SELECT Racename, RaceDate FROM race ORDER BY RaceDate DESC")
    for (rn, rd) in cursor:
        r_id = get_id(10)
        races[r_id] = (rn + ", " + str(rd))
        rid[r_id] = [rn, rd]
    race_choice = ui.select(options= races, label='Choose Race', with_input=True)
    button = ui.button('Submit')
    ### maybe just modify this for filter_athlete query ###
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
    ui.run()

#################################################

ui.link('Insert Athlete', ins_athlete_page)
ui.link('Insert Race', ins_race_page)
ui.link('Insert Race Results', ins_results_page)

ui.link('Update Athlete', upd_athlete_page)
ui.link('Update Race', upd_race_page)

ui.link('Delete Athlete', del_athlete_page)
ui.link('Delete Race', del_race_page)
ui.link('Delete Race Results', del_results_page)
ui.link('View Race Results', race_results_page)

ui.link('All Results', all_results_page)
ui.run()