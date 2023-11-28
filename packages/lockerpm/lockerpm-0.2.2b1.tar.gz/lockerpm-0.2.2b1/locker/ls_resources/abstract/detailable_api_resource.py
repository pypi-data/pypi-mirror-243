from __future__ import absolute_import, division, print_function

from locker.ls_resources.abstract.api_resource import APIResource


class DetailableAPIResource(APIResource):
    @classmethod
    def retrieve(cls, id, access_key_id=None, access_key_secret=None, **params):
        return super().retrieve(id, access_key_id, access_key_secret, **params)
