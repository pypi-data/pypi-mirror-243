from enum import Enum

from MSApi.MSLowApi import MSLowApi, error_handler
from MSApi.Currency import Currency
from MSApi.ObjectMS import ObjectMS, check_init
from MSApi.Meta import Meta
from MSApi.PriceType import PriceType
from MSApi.CustomEntity import CustomEntity


class DiscountStrategy(Enum):
    e_by_sum = "bySum"
    e_by_priority = "byPriority"


class CompanySettings(ObjectMS):
    _type_name = 'companysettings'

    @classmethod
    def get_company_settings(cls):
        """Запрос на получение Настроек компании."""
        response = MSLowApi.auch_get('context/companysettings')
        error_handler(response)
        return CompanySettings(response.json())

    @classmethod
    def get_default_price_type(cls) -> PriceType:
        """Получить тип цены по умолчанию"""
        response = MSLowApi.auch_get('context/companysettings/pricetype/default')
        error_handler(response)
        return PriceType(response.json())

    @classmethod
    def gen_custom_entities(cls):
        response = MSLowApi.auch_get("context/companysettings/metadata")
        error_handler(response)
        for entity_json in response.json().get('customEntities', []):
            yield CustomEntity(entity_json)

    @check_init
    def get_currency(self) -> Currency:
        """Cтандартная валюта"""
        return Currency(self._json.get('currency'))

    @check_init
    def gen_price_types(self):
        """Коллекция всех существующих типов цен."""
        for price_type in self._json.get('priceTypes'):
            yield PriceType(price_type)

    @check_init
    def get_discount_strategy(self) -> DiscountStrategy:
        """Совместное применение скидок."""
        return DiscountStrategy(self._json.get('discountStrategy'))

    @check_init
    def get_global_operation_numbering(self) -> bool:
        """Использовать сквозную нумерацию документов.
        Если проставлен true, будет установлена сквозная нумерация за всю историю,
        иначе нумерация документов будет начинаться заново каждый календарный год."""
        return bool(self._json.get('globalOperationNumbering'))




