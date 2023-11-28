import os
from dotenv import load_dotenv

from locker import Locker


load_dotenv()
access_key_id = os.getenv("ACCESS_KEY_ID")
access_key_secret = os.getenv("ACCESS_KEY_SECRET")
headers = {
    "cf-access-client-id": os.getenv("CF_ACCESS_CLIENT_ID"),
    "cf-access-client-secret": os.getenv("CF_ACCESS_CLIENT_SECRET")
}

locker = Locker(access_key_id=access_key_id, access_key_secret=access_key_secret, options={"headers": headers})


# List environments
environments = locker.list_environments()
for environment in environments:
    print(environment.name, environment.external_url, environment.description)


# Get an environment by name
environment = locker.get_environment("staging2")
if environment:
    print(environment.name, environment.external_url, environment.description)
else:
    print("The environment does not exist")


# Update an environment by name
environment = locker.modify_environment(name="staging", external_url="staging.demo.environment")
print(environment.name, environment.external_url, environment.description)


# Create new environment
new_environment = locker.create_environment(name="production", external_url="prod.demo.environment")
print(new_environment.name, new_environment.external_url, new_environment.description)
