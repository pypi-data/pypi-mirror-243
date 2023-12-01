from typing import Optional

from MSApi.MSApi import MSApi

from MSApi.ObjectMS import ObjectMS, SubObjectMS
from MSApi.ProductFolder import ProductFolder
from MSApi.PriceType import PriceType
from MSApi.Meta import Meta

from MSApi.mixin.GenListMixin import GenerateListMixin
from MSApi.mixin.CreateNewMixin import CreateNewMixin
from MSApi.mixin.NameMixin import NameMixin
from MSApi.mixin.AccountIdMixin import AccountIdMixin


class SpecialPrice(SubObjectMS):

    def get_price_type(self) -> PriceType:
        return PriceType(self._json.get('priceType'))

    def get_value(self) -> Optional[float]:
        value = self._json.get('value')
        if value is None:
            return None
        return float(value) / 100


class DiscountLevel(SubObjectMS):

    def get_amount(self) -> float:
        """Сумма накоплений"""
        return float(self._json.get('amount')) / 100

    def get_discount(self) -> Optional[float]:
        """Процент скидки, соответствующий данной сумме"""
        discount = self._json.get('discount')
        if discount is None:
            return None
        return float(discount) / 100


class Discount(ObjectMS,
               GenerateListMixin,
               CreateNewMixin,
               NameMixin,
               AccountIdMixin):
    _type_name = 'discount'

    def is_active(self) -> bool:
        return bool(self._json.get('active'))

    def is_all_products(self) -> bool:
        return bool(self._json.get('allProducts'))

    def is_all_agents(self) -> bool:
        return bool(self._json.get('allAgents'))

    def gen_agent_tags(self):
        tags = self._json.get('agentTags')
        if tags is None:
            return
        for tag in tags:
            yield tag

    def gen_assortment(self):
        objects = self._json.get('assortment')
        if objects is None:
            return
        for obj in objects:
            yield MSApi.get_object_by_meta(Meta(obj.get('meta')))


class SpecialPriceDiscount(Discount):
    _type_name = 'specialpricediscount'

    def gen_productfolders(self):
        """Группы товаров, к которым применяется скидка, если применяется не ко всем товарам"""
        productfolders = self._json.get('productFolders')
        if productfolders is None:
            return
        for productfolder in productfolders:
            yield ProductFolder(productfolder)

    def get_discount_percent(self) -> Optional[float]:
        """Процент скидки если выбран фиксированный процент"""
        discount = self._json.get('discount')
        if discount is None:
            return None
        return discount / 100

    def get_special_price(self) -> Optional[SpecialPrice]:
        """Спец. цена (если выбран тип цен)."""
        special_price = self._json.get('specialPrice')
        if special_price is None:
            return None
        return SpecialPrice(special_price)

    def is_use_price_type(self):
        return bool(self._json.get('usePriceType'))


class AccumulationDiscount(Discount):
    _type_name = 'accumulationdiscount'

    def gen_productfolders(self):
        """Группы товаров, к которым применяется скидка, если применяется не ко всем товарам"""
        productfolders = self._json.get('productfolders')
        if productfolders is None:
            return
        for productfolder in productfolders:
            yield ProductFolder(productfolder)

    def gen_levels(self):
        """Проценты скидок при определенной сумме продаж."""
        level = self._json.get('levels')
        if level is None:
            return None
        return DiscountLevel(level)