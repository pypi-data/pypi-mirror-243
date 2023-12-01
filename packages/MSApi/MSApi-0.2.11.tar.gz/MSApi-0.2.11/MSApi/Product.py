from typing import Optional

from MSApi.mixin import AttributeMixin, SalePricesMixin
from MSApi.Assortment import Assortment
from MSApi.ProductFolder import ProductFolder
from MSApi.ObjectMS import check_init
from MSApi.mixin.GenListMixin import GenerateListMixin
from MSApi.mixin.RequestByIdMixin import RequestByIdMixin
from MSApi.mixin.ProductfolderMixin import ProductfolderMixin
from MSApi.mixin.NameMixin import NameMixin
from MSApi.mixin.CreateNewMixin import CreateNewMixin


class Product(Assortment,
              AttributeMixin,
              SalePricesMixin,
              RequestByIdMixin,
              GenerateListMixin,
              ProductfolderMixin,
              NameMixin,
              CreateNewMixin):

    _type_name = 'product'

    def __init__(self, json):
        super().__init__(json)

    def __str__(self):
        self.get_name()

    @check_init
    def get_description(self) -> Optional[str]:
        return self._json.get('description')

    @check_init
    def get_variants_count(self) -> int:
        return int(self._json.get('variantsCount'))

    @check_init
    def get_article(self) -> Optional[str]:
        return self._json.get('article')

    @check_init
    def get_code(self) -> Optional[str]:
        return self._json.get('code')

    def has_variants(self) -> bool:
        return self.get_variants_count() > 1
