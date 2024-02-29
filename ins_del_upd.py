from nicegui import ui

def submitInsert():
    #SQL Insert
    #PopUp saying added
    #return to homepage
    return None

#insert athlete
@ui.page('/ins_athlete_page')
def ins_athlete_page():
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

    #this is where you need to implement the SQL Insertion, at the on-click.
    # I'd say make a function (above) and utilize fn_input.value, ln_input.value, etc.
    #Then return to home page
    submit = ui.button('Submit', on_click = lambda: ui.notify('Button Clicked!'))

#################################################
    
#delete athlete
@ui.page('/del_athlete_page')
async def del_athlete_page():
    ui.label('Choose Athlete to Delete')
    # need a select all athletes query to put them into athletes, maybe First, Last, Grad Year
    # my only concern is we probably want to use the 'ID' to delete in case of rare same name/year combos
    # we need to specify a dictionary mapping values to labels where value is id and label is name and year
    athletes = {1:'John Smith 2024', 2: 'Jackson Livanec 2024'}
    result = 0
    del_athlete = ui.select(options= athletes, label='Choose Athlete', with_input=True).bind_value_to(globals(), 'result')
    # here, we need to add an 'on_change' parameter calling a function to query the specific athlete based on id (the binding 
    # should always update result any time the selection is changed)
    
    delete = ui.button('Delete', color='red', on_click = lambda: ui.notify('Delete Button Clicked!  ' + str(del_athlete.value)))

#################################################
    
#update athlete
@ui.page('/upd_athlete_page')
async def upd_athlete_page():
    ui.label('Choose Athlete to Update')
    # need a select all athletes query to put them into athletes, maybe First, Last, Grad Year
    # my only concern is we probably want to use the 'ID' to delete in case of rare same name/year combos
    # we need to specify a dictionary mapping values to labels where value is id and label is name and year
    athletes = {1:'John Smith 2024', 2: 'Jackson Livanec 2024'}
    result = 0
    upd_athlete = ui.select(options= athletes, label='Choose Athlete', with_input=True).bind_value_to(globals(), 'result')
    # here, we need to add an 'on_change' parameter calling a function to query the specific athlete based on id (the binding 
    # should always update result any time the selection is changed)
    
    delete = ui.button('Delete', color='red', on_click = lambda: ui.notify('Delete Button Clicked!  ' + str(upd_athlete.value)))

    
    update = ui.button('Edit', color='red', on_click = lambda: ui.notify('Edit Button Clicked!  ' + str(upd_athlete.value)))


    await update.clicked()
    fn_input = ui.input(label='First Name', placeholder='e.g. John', validation={'Input too long': lambda value: len(value) <= 20})
    ln_input = ui.input(label='Last Name', placeholder='e.g. Smith', validation={'Input too long': lambda value: len(value) <= 20})
    grad_input = ui.number(label='Graduation Year', placeholder='e.g. 2024', min=1000, max=9999, 
                           precision=0, validation={'Please enter valid year': lambda value: value > 999 and value < 10000}).bind_value_from(globals(), 'result')
    home_input = ui.input(label='Hometown', placeholder='e.g. Blacksburg, VA', validation={'Input too long': lambda value: len(value) <= 20})
    ui.label('Sex')
    sex_input = ui.toggle({'M': 'Male', 'F': 'Female', 'O': 'Other'}, value='M')
    with ui.input('Date of Birth') as date:
        with date.add_slot('append'):
            ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
        with ui.menu() as menu:
            ui.date().bind_value(date)



ui.link('Insert Athlete', ins_athlete_page)
ui.link('Delete Athlete', del_athlete_page)
ui.link('Update Athlete', upd_athlete_page)

ui.run()