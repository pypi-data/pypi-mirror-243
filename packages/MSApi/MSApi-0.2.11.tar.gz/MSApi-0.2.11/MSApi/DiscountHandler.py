
from typing import Union

from MSApi.mixin.SalePricesMixin import SalePricesMixin
from MSApi.PriceType import PriceType
from MSApi.CompanySettings import CompanySettings
from MSApi.Discount import SpecialPriceDiscount
from MSApi.exceptions import MSApiException


def check_init(f):
    def wrapper(*args):
        if not args[0].is_init:
            args[0].init()
        return f(*args)
    return wrapper


class DiscountHandler:
    __active_discounts: [SpecialPriceDiscount] = []
    __default_price_type: PriceType = None
    is_init = False

    @classmethod
    def init(cls):
        for discount in SpecialPriceDiscount.gen_list():
            if not discount.is_active():
                continue
            cls.__active_discounts.append(discount)
        cls.__default_price_type = CompanySettings.get_default_price_type()
        cls.is_init = True

    @classmethod
    @check_init
    def get_default_price_type(cls) -> PriceType:
        return cls.__default_price_type

    @classmethod
    @check_init
    def get_default_price_value(cls, assort: SalePricesMixin):
        for sale_price in assort.gen_sale_prices():
            if sale_price.get_price_type() == cls.__default_price_type:
                return sale_price.get_value()
        else:
            raise MSApiException(f"Default price type in {str(assort)} not found")

    @classmethod
    @check_init
    def get_actual_price(cls, assort: SalePricesMixin, counterparty_group_tag: str) -> float:
        max_discount_percent: float = 0
        discount_price_types: [PriceType] = []

        for discount in cls.__active_discounts:
            if cls.__is_discount_included_agent_group(discount, counterparty_group_tag) \
                    and cls.__is_discount_included_assort(discount, assort):
                if discount.is_use_price_type():
                    # TODO обработка параметра value
                    price_type = discount.get_special_price().get_price_type()
                    if price_type not in discount_price_types:
                        discount_price_types.append(price_type)
                else:
                    disc_percent = discount.get_discount_percent() or 0
                    if disc_percent > max_discount_percent:
                        max_discount_percent = disc_percent

        min_price = current_price = cls.get_default_price_value(assort)

        for sale_price in assort.gen_sale_prices():
            value = sale_price.get_value()
            if sale_price.get_price_type() in discount_price_types:
                if min_price > value:
                    min_price = value

        percent_sale_price = current_price * (1 - max_discount_percent)
        if min_price > percent_sale_price:
            min_price = percent_sale_price

        return round(min_price * 100) / 100

    @staticmethod
    def __is_discount_included_agent_group(discount: SpecialPriceDiscount, agent_group: str) -> bool:
        return discount.is_all_agents() or (agent_group in discount.gen_agent_tags())

    @staticmethod
    def __is_discount_included_assort(discount: SpecialPriceDiscount,
                                      assort) -> bool:
        if discount.is_all_products():
            return True
        for obj in discount.gen_assortment():
            if obj == assort:
                return True

        if hasattr(type(assort), 'get_productfolder'):
            productfolder = assort.get_productfolder()
        elif hasattr(type(assort), 'get_product'):
            product = assort.get_product()
            productfolder = product.get_productfolder()
        else:
            raise MSApiException(f"Unexpected type {type(assort)}")
        for disc_folder in discount.gen_productfolders():
            if productfolder == disc_folder:
                return True
        return False
