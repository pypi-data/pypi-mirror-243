from typing import Union


from MSApi.ObjectMS import ObjectMS, check_init
from MSApi.mixin.NameMixin import NameMixin


class Attribute(ObjectMS,
                NameMixin):

    @check_init
    def get_value(self) -> Union[str]:
        return self._json.get('value')

    @check_init
    def get_type(self) -> Union[str]:
        return self._json.get('type')
