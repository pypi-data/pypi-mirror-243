from datetime import datetime
from typing import Optional

from MSApi.Meta import Meta
from MSApi.ObjectMS import ObjectMS, check_init
from MSApi.MSLowApi import MSLowApi, error_handler, string_to_datetime

from MSApi.mixin.NameMixin import NameMixin


class CustomEntityElement(ObjectMS):

    @check_init
    def get_account_id(self) -> str:
        return self._json.get('accountId')

    @check_init
    def get_name(self) -> str:
        return self._json.get('name')

    @check_init
    def get_updated_time(self) -> datetime:
        return string_to_datetime(self._json.get('updated'))

    @check_init
    def get_description(self) -> Optional[str]:
        return self._json.get('description')

    @check_init
    def get_code(self) -> Optional[str]:
        return self._json.get('code')

    @check_init
    def get_external_code(self) -> Optional[str]:
        return self._json.get('externalCode')


class CustomEntity(ObjectMS, NameMixin):

    def get_entity_meta(self) -> Meta:
        return Meta(self._json.get('entityMeta'))

    def gen_elements(self):
        elements_json = MSLowApi.get_json_by_href(self.get_entity_meta().get_href())
        for element_json in elements_json.get('rows', []):
            yield CustomEntityElement(element_json)

