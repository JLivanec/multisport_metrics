from nicegui import ui
from nicegui.events import ValueChangeEventArguments
import mysql.connector

def connect(container):
    global cnx
    cnx = mysql.connector.connect(
        #change password, database
        host='localhost',
        user='root',
        password="",
        port='3306',
        database='multisport_metrics',
        auth_plugin='mysql_native_password'
    )
    if cnx.is_connected():
        ui.notify("You have been connected!")
        with container:
            ui.icon('thumb_up')
            ui.markdown('Database Connected')
            #ui.button('Tables', on_click=lambda:tables(container))
    else:
        ui.notify("Connection Failed!")
    #mycursor = connector.cursor()
    #mycursor.execute("SELECT FirstName FROM athlete")
    #data = mycursor.fetchall()
    #for dat in data:
    #    print("Name:", dat[0])

def disconnect(container):
    container.clear()
    ui.notify("You have been disconnected")
    cnx.close()

def tables(container):
    tbs = cnx.cmd_query("GET TABLES")
    ui.notify(tbs)


ui.run()

def main():
    ui.markdown('''# Multisport Metrics
                
    Jackson Livanec and Chris Mascis''')
    
    with ui.row():
        ui.button('Connect', on_click=lambda:connect(res_container))
        ui.button('Disconnect', on_click=lambda:disconnect(res_container))
    res_container = ui.column()

    #ui.markdown('Jackson Livanec, Chris Mascis')
    #ui.link('Source Code', 'https://github.com/jinzzasol/Mathsage').classes('mt-8')
    ui.run()


main()