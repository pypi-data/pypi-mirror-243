from MSApi.ObjectMS import ObjectMS

from MSApi.mixin.GenListMixin import GenerateListMixin
from MSApi.mixin.AttributeMixin import AttributeMixin
from MSApi.mixin.StateMixin import StateMixin
from MSApi.mixin.RequestByIdMixin import RequestByIdMixin


class CashOut(ObjectMS,
              AttributeMixin,
              GenerateListMixin,
              RequestByIdMixin,
              StateMixin):

    _type_name = 'cashout'
