import os
from dotenv import load_dotenv

from locker import Locker
from locker.error import APIError


load_dotenv()
access_key_id = os.getenv("ACCESS_KEY_ID")
access_key_secret = os.getenv("ACCESS_KEY_SECRET")
headers = {
    "cf-access-client-id": os.getenv("CF_ACCESS_CLIENT_ID"),
    "cf-access-client-secret": os.getenv("CF_ACCESS_CLIENT_SECRET")
}

locker = Locker(access_key_id=access_key_id, access_key_secret=access_key_secret, options={"headers": headers})
# locker.log = 'debug'

# List secrets
secrets = locker.list()
for secret in secrets:
    print(secret.key, secret.value, secret.description, secret.environment_name)


# Get a secret value by secret key. If the Key does not exist, the SDK will return the default_value
secret_value = locker.get_secret("REDIS_CONNECTION", default_value="TheDefaultValue")
print(secret_value)


# Get a secret value by secret key and specific environment name.
# If the Key does not exist, the SDK will return the default_value
secret_value = locker.get_secret("MYSQL_CONNECTION", environment_name="staging", default_value="TheDefaultValue")
print(secret_value)


# Update a secret value by secret key
secret = locker.modify(key="MYSQL_CONNECTION", environment_name="staging", value="mysql_value")
print(secret.key, secret.value, secret.description, secret.environment_name)


# Create new secret and handle error
try:
    new_secret = locker.create(key="GOOGLE_API", value="my_google_api", environment_name="staging")
    print(new_secret.key, new_secret.value, new_secret.description, new_secret.environment_name)
except APIError as e:
    print(e.user_message)
    print(e.http_body)
