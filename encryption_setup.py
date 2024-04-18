#run this first

from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
# copy the printed out key into a file called .env like this:
# CRYPT_SECRET_KEY=YOUR_KEY_HERE



# once you've done the above, comment it out and uncomment this
'''import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

# Retrieve the secret key from an environment variable
secret_key = os.environ.get('CRYPT_SECRET_KEY')
cipher_suite = Fernet(secret_key)
password = 'abc123'
encrypt_password = cipher_suite.encrypt(password.encode()).decode()
print(encrypt_password)
# copy this printed encrypted password into the password field for user1 in the dump_all.sql


#lastly either use dump_all again or just make the new users table and insert user 1
'''