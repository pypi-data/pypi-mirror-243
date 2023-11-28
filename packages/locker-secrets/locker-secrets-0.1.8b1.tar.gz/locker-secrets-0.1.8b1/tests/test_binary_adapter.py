import os
import sys

from dotenv import load_dotenv
from locker.binary_adapter import BinaryAdapter


class TestBinaryAdapter(object):
    def test_get_platform(self):
        load_dotenv()
        access_key_id = os.getenv("ACCESS_KEY_ID")
        access_key_secret = os.getenv("ACCESS_KEY_SECRET")

        binary_adapter = BinaryAdapter(
            access_key_id=access_key_id, access_key_secret=access_key_secret
        )
        platform = binary_adapter.get_platform()
        return platform == sys.platform

    def test_get_sdk_version(self):
        load_dotenv()
        access_key_id = os.getenv("ACCESS_KEY_ID")
        access_key_secret = os.getenv("ACCESS_KEY_SECRET")

        binary_adapter = BinaryAdapter(
            access_key_id=access_key_id, access_key_secret=access_key_secret
        )
        sdk_version = binary_adapter.get_sdk_version()
        assert isinstance(sdk_version, str) and len(sdk_version.split(".")) == 3

    def test_call(self):
        load_dotenv()
        access_key_id = os.getenv("ACCESS_KEY_ID")
        access_key_secret = os.getenv("ACCESS_KEY_SECRET")
        api_base = os.getenv("API_BASE") or "ht"

        binary_adapter = BinaryAdapter(
            access_key_id=access_key_id, access_key_secret=access_key_secret,
            api_base=""
        )

        cli_ = '%s get --id "%s"' % (base, key)
