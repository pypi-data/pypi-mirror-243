
from MSApi.ObjectMS import ObjectMS, check_init

from MSApi.mixin.NameMixin import NameMixin
from MSApi.mixin.GenListMixin import GenerateListMixin


class ProductFolder(ObjectMS,
                    NameMixin,
                    GenerateListMixin):
    _type_name = 'productfolder'