from cryptography.fernet import Fernet
from configparser import ConfigParser
import tracemalloc
tracemalloc.start()


# Load the key
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

# Login credentials
config = ConfigParser()
config.read('config.ini')
username = cipher_suite.decrypt(config['X']['username']).decode()
password = cipher_suite.decrypt(config['X']['password']).decode()
email = cipher_suite.decrypt(config['X']['email']).decode()

print(f'username: {username}')
print(f'password: {password}')
print(f'email: {email}')