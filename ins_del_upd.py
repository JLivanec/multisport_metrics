from nicegui import ui
import mysql.connector
from nicegui.events import ValueChangeEventArguments
import random as rand
from datetime import date, datetime, timedelta


def connect():
    global cnx
    global cursor
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password="",
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

def remove_athlete(a_id, athletes):
    query = "DELETE FROM athlete WHERE (AthleteID = %s)"
    athlete_id = (a_id,)
    cursor.execute(query, athlete_id)
    ui.notify("Deleted Athlete " + athletes[a_id])
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
                           precision=0, validation={'Please enter valid year': lambda value: value > 999 and value < 10000})
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
async def del_athlete_page():
    if not is_connected():
        connect()
    ui.label('Choose Athlete to Delete')
    athletes = {}
    cursor.execute("SELECT AthleteID, FirstName, LastName FROM athlete ORDER BY LastName ASC")
    for (a_id, fn, ln) in cursor:
        athletes[a_id] = (ln + ", " + fn)

    result = 0
    del_athlete = ui.select(options= athletes, label='Choose Athlete', with_input=True).bind_value_to(globals(), 'result')
    
    ui.button('Delete', color='red', on_click = lambda: remove_athlete(del_athlete.value, athletes))

#################################################
    
#update athlete
@ui.page('/upd_athlete_page')
async def upd_athlete_page():
    if not is_connected():
        connect()
    ui.label('Choose Athlete to Update')
    athletes = {}
    cursor.execute("SELECT AthleteID, FirstName, LastName FROM athlete ORDER BY LastName ASC")
    for (a_id, fn, ln) in cursor:
        athletes[a_id] = (ln + ", " + fn)
    result = 0
    upd_athlete = ui.select(options= athletes, label='Choose Athlete', with_input=True).bind_value_to(globals(), 'result')
    # here, we need to add an 'on_change' parameter calling a function to query the specific athlete based on id (the binding 
    # should always update result any time the selection is changed)
    
    ui.button('Delete', color='red', on_click = lambda: remove_athlete(upd_athlete.value, athletes))

    
    update = ui.button('Edit', color='red', on_click = None)


    await update.clicked()
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

    ui.button('Confirm Changes', color='red', on_click = lambda: update_athlete(upd_athlete.value, fn_input.value,
                                                                                ln_input.value, grad_input.value, home_input.value,
                                                                                sex_input.value, date.value))


ui.link('Insert Athlete', ins_athlete_page)
ui.link('Delete Athlete', del_athlete_page)
ui.link('Update Athlete', upd_athlete_page)

ui.run()