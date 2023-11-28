from __future__ import absolute_import, division, print_function

from locker.ls_resources.abstract.api_resource import APIResource


class CreateableAPIResource(APIResource):
    @classmethod
    def create(cls, access_key_id=None, access_key_secret=None, api_base=None, api_version=None, **params):
        return cls._static_call(
            f"{cls.class_cli()} create",
            access_key_id,
            access_key_secret,
            api_base=api_base,
            api_version=api_version,
            params=params,
        )
