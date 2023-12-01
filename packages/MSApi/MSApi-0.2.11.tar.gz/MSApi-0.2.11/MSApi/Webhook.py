from MSApi.MSApi import MSApi
from MSApi.ObjectMS import ObjectMS

from MSApi.mixin.GenListMixin import GenerateListMixin
from MSApi.mixin.RequestByIdMixin import RequestByIdMixin


class Webhook(ObjectMS,
              GenerateListMixin,
              RequestByIdMixin):

    _type_name = 'webhook'

    def get_action(self):
        return self.get_json()['action']

    def get_diff_type(self):
        return self.get_json().get('diffType')

    def is_enabled(self):
        return bool(self.get_json()['enabled'])

    def get_entity_type(self):
        return MSApi.get_object_type(self.get_json()['entityType'])

    def get_method(self):
        return self.get_json()['method']

    def get_url(self):
        return self.get_json()['url']
