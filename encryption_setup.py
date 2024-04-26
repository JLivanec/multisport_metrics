# run this first
#'''
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
# copy the printed out key into a file called .env in root folder exactly like this:
# CRYPT_SECRET_KEY=YOUR_KEY_HERE
# do not use spaces, do not use ' or " characters
# your key will most likely end with =
#'''

###########################################################
'''
# once you've done the above, comment it out and uncomment this

import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
load_dotenv()

# Retrieve the secret key from an environment variable
secret_key = os.environ.get('CRYPT_SECRET_KEY')
cipher_suite = Fernet(secret_key)
# enter your desired admin password here
password = 'yourpasswordhere'
encrypt_password = cipher_suite.encrypt(password.encode()).decode()
print(encrypt_password)
# copy this printed encrypted password into the password field for the User at the bottom of sql_dumps/dump_all.sql


# sign in and navigate to your database called multisport_metrics (create if not created) with: use multisport_metrics;
# use the dump_all.sql file as the source for your database with: source whatever/your/path/is/to/sql_dumps/dump_all.sql;
'''