from typing import Optional

from MSApi.Assortment import Assortment
from MSApi.mixin import AttributeMixin, SalePricesMixin, GenerateListMixin, ProductfolderMixin
from MSApi.mixin.NameMixin import NameMixin


class Bundle(Assortment,
             AttributeMixin,
             SalePricesMixin,
             GenerateListMixin,
             ProductfolderMixin,
             NameMixin):

    _type_name = 'bundle'
