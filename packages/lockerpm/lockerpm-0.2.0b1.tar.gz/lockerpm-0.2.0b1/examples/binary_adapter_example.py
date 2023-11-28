import os
from dotenv import load_dotenv

from locker.binary_adapter import BinaryAdapter


load_dotenv()
access_key = os.getenv("ACCESS_KEY_TEST")
api_base = "https://secrets-core.locker.io"
api_version = None

binary_adapter = BinaryAdapter(
    access_key_id=access_key, api_base=api_base, api_version=api_version
)
cli = "secret list"
output_data = binary_adapter.call(
    cli, asjson=False
)

print(output_data)
