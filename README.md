# MultiSport Metrics
By **Christopher Mascis and Jackson Livanec**
### Setup for your local machine:
1. Clone Repository from github to your local machine.  
    - **There will be no need to navigate away from the base directory of the project**
2. Set up virtual environment in base directory if you'd like 
3. Install all requirements from requirements.txt  
    - In the terminal with virtual environment activated, `pip install -r requirements.txt`  
4. Set up your initial admin user account for the app.  
    1. Open encryption_setup.py
    2. Run the file as is
    3. Copy the printed encryption key into a new file called **.env** in the root folder
        - your file should be one line and look like this `CRYPT_SECRET_KEY=YOUR_KEY_HERE`
        - do not use spaces, do not use ' or " characters  
        - your key will most likely end with =  
    4. Following directions comment the first chunk in the file and uncomment the second chunk. Run the file.  
        - copy the printed encrypted password, you'll need this  
    5. Navigate to sql_dumps/dump_all.sql file, and scroll all the way to the bottom
    6. You should see an insert statment with a prompt that says **YOUR ENCRYPTED PASSWORD HERE**. Replace the prompt with that weird thing you just copied.
    7. sign in and navigate to your database called **multisport_metrics** (create if not created) with: `use multisport_metrics;`  
    8. use the dump_all.sql file as the source for your database with: `source whatever/your/path/is/to/sql_dumps/dump_all.sql;`  
        - exit from mysql after this is complete  
5. Go to main.py and towards the top of the file fill in your mysql database information
6. run `python main.py` to start the app, it should load in a browser window. Sign in with username: admin and whatever your password is.  
    - might take a bit to load for the first time running  
    - once signed in you can create your own personal user account under the admin tools menu.
