from MSApi.Employee import Employee

from MSApi.Meta import Meta
from MSApi.MSApi import MSApi
from MSApi.ObjectMS import ObjectMS, check_init

from MSApi.mixin.AccountIdMixin import AccountIdMixin
from MSApi.mixin.CreateNewMixin import CreateNewMixin
from MSApi.mixin.GenListMixin import GenerateListMixin
from MSApi.mixin.DescriptionMixin import DescriptionMixin
from MSApi.mixin.RequestByIdMixin import RequestByIdMixin


class Task(ObjectMS,
           AccountIdMixin,
           CreateNewMixin,
           GenerateListMixin,
           DescriptionMixin,
           RequestByIdMixin):

    _type_name = 'task'
    _necessary_when_creating = ['assignee', 'description', ]

    @check_init
    def get_agent(self):
        data = self.get_json().get('agent')
        if data is None:
            return None
        return MSApi.get_object_by_meta(Meta(data))

    @check_init
    def get_assignee(self):
        return Employee(self._json['assignee'])
