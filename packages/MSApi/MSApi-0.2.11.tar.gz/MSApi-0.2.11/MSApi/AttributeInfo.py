

from MSApi.ObjectMS import ObjectMS, check_init

from MSApi.mixin.NameMixin import NameMixin
from MSApi.mixin.DescriptionMixin import DescriptionMixin


class AttributeInfo(ObjectMS,
                    NameMixin,
                    DescriptionMixin):

    @check_init
    def get_type(self) -> str:
        return self._json.get('type')

    @check_init
    def is_required(self) -> bool:
        return self._json.get('required')
