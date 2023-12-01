from MSApi.ObjectMS import ObjectMS, check_init
from MSApi.MSLowApi import MSLowApi, error_handler
from MSApi.Employee import Employee
from MSApi.Meta import Meta
from typing import Optional

from MSApi.mixin.AccountIdMixin import AccountIdMixin
from MSApi.mixin.IsSharedMixin import IsSharedMixin
from MSApi.mixin.NameMixin import NameMixin
from MSApi.mixin.GenListMixin import GenerateListMixin
from MSApi.mixin.CreateNewMixin import CreateNewMixin
from MSApi.mixin.RequestByIdMixin import RequestByIdMixin


class Account(ObjectMS,
              AccountIdMixin):
    _type_name = 'account'

    @check_init
    def get_account_number(self) -> str:
        return self._json.get('accountNumber')


class Organization(ObjectMS,
                   GenerateListMixin,
                   CreateNewMixin,
                   AccountIdMixin,
                   IsSharedMixin,
                   RequestByIdMixin,
                   NameMixin):
    """Юрлицо"""
    _type_name = 'organization'

    @check_init
    def get_owner(self) -> Optional[Employee]:
        return Employee(self._json.get('owner'))

    @check_init
    def get_group(self) -> Optional[Meta]:
        return self._json.get('group')

    def gen_accounts(self):
        response = MSLowApi.auch_get(f"entity/organization/{self.get_id()}/accounts")
        error_handler(response)
        for account_json in response.json()["rows"]:
            yield Account(account_json)

