from typing import Optional

from MSApi.ObjectMS import ObjectMS, check_init

from MSApi.mixin.GenListMixin import GenerateListMixin
from MSApi.mixin.RequestByIdMixin import RequestByIdMixin
from MSApi.mixin.CreateNewMixin import CreateNewMixin
from MSApi.mixin.AccountIdMixin import AccountIdMixin
from MSApi.mixin.NameMixin import NameMixin


class Employee(ObjectMS,
               GenerateListMixin,
               RequestByIdMixin,
               CreateNewMixin,
               AccountIdMixin,
               NameMixin):
    _type_name = "employee"

    @check_init
    def get_owner(self):
        return self._get_optional_object('owner', Employee)

    @check_init
    def get_shared(self) -> bool:
        return self._json.get('shared')