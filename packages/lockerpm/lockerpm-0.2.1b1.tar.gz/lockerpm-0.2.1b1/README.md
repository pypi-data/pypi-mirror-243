# Locker Secret Python SDK

<p align="center">
  <img src="https://cystack.net/images/logo-black.svg" alt="CyStack" width="50%"/>
</p>

 
---

The Locker Secret Python SDK provides convenient access to the Locker Secret API from applications written in the 
Python language. It includes a pre-defined set of classes for API resources that initialize themselves dynamically 
from API responses which makes it compatible with a wide range of versions of the Locker Secret API.


## The Developer - CyStack

The Locker Secret Python SDK is developed by CyStack, one of the leading cybersecurity companies in Vietnam. 
CyStack is a member of Vietnam Information Security Association (VNISA) and Vietnam Association of CyberSecurity 
Product Development. CyStack is a partner providing security solutions and services for many large domestic and 
international enterprises.

CyStack’s research has been featured at the world’s top security events such as BlackHat USA (USA), 
BlackHat Asia (Singapore), T2Fi (Finland), XCon - XFocus (China)... CyStack experts have been honored by global 
corporations such as Microsoft, Dell, Deloitte, D-link...


## Documentation

The documentation will be updated later.

## Requirements

- Python 3.6+

## Installation

Install from PyPip:

```
pip install --upgrade lockerpm
```

Install from source with:

```
python setup.py install
```

## Usages

### Set up access key

The SDK needs to be configured with your access key which is available in your Locker Secret Dashboard. 
Initialize the `access_key` to its value. 
You also need to set `api_base` value (default is `https://api.locker.io/locker_secrets`).

If you need to set your custom headers, you also need to set `headers` value in the `options` param:

```
from locker import Locker

access_key_id = "your_access_key_id..."
access_key_secret = "your_access_key_secret..."
api_base = "your_base_api.host"
headers = {
    "cf-access-client-id": "",
    "cf-access-client-secret": ""
}

locker = Locker(
    access_key_id=access_key_id, 
    access_key_secret=access_key_secret, 
    api_base=api_base, 
    options={"headers": headers}
)
```

Now, you can use SDK to get or set values:

```
# Get list secrets quickly
secrets = locker.list()

# Get a secret value by secret key. 
# If the Key does not exist, SDK will return the default_value
secret_value = locker.get_secret("REDIS_CONNECTION", default_value="TheDefaultValue")
print(secret_value)

# Get a secret value by secret key and specific environment name.
# If the Key does not exist, SDK will return the default_value
secret_value = locker.get_secret("REDIS_CONNECTION", environment_name="staging", default_value="TheDefaultValue")
print(secret_value)

# Create new secret
secret = locker.create(key="YOUR_NEW_SECRET_KEY", value="YOUR_NEW_SECRET_VALUE")

# Update new secret
secret = locker.modify(key="YOUR_NEW_SECRET_KEY", value="UPDATED_SECRET_VALUE")

# Update a secret value by secret key and a specific environment name
secret = locker.modify(key="REDIS_CONNECTION",  environment_name="staging", value="staging.redis.connection")
print(secret.key, secret.value, secret.environment_name)

# List environments
environments = locker.list_environments()

# Get an environment object by name
environment = locker.get_environment("prod")

# Create new environment
new_environment = locker.create_environment(name="staging", external_url="staging.host")

# Update an environment by name
environment = locker.modify_environment(name="staging", external_url="new.staging.host")
```

### Logging

The library can be configured to emit logging that will give you better insight into what it's doing. 
There are some levels: `debug`, `info`, `warning`, `error`.

The `info` logging level is usually most appropriate for production use, 
but `debug` is also available for more verbosity.

There are a few options for enabling it:

1. Set the environment variable `LOCKER_LOG` to the value `debug`, `info`, `warning` or `error`

```sh
$ export LOCKER_LOG=debug
```

2. Set `log` when initializing the Locker object:

```python
from locker import Locker

locker = Locker(log="debug")
```

3. Enable it through Python's logging module:

```python
import logging
logging.basicConfig()
logging.getLogger('locker').setLevel(logging.DEBUG)
```


## Examples

See the [examples' folder](/examples).

## Development

First install for development.
```
pip install -r requirements-dev.txt
```

### Run tests

Test by using tox. We test against the following versions.
- 3.6
- 3.7
- 3.8
- 3.9
- 3.10

To run all tests against all versions, use:
```
tox
```

Run all tests for a specific Python version:
```
tox -e py3.10
```

Run all tests in a single file:
```
tox -e py3.10 -- tests/test_util.py
```


## Reporting security issues

We take the security and our users' trust very seriously. If you found a security issue in Locker SDK Python, please 
report the issue by contacting us at <contact@locker.io>. Do not file an issue on the tracker. 


## Contributing

Please check [CONTRIBUTING](CONTRIBUTING.md) before making a contribution.


## Help and media

- FAQ: https://support.locker.io

- Community Q&A: https://forum.locker.io

- News: https://locker.io/blog


## License
