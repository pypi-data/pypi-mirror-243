from MSApi.MSLowApi import caching, MSLowApi
from MSApi.Template import Template
from MSApi.ObjectMS import ObjectMS

from MSApi.mixin.RequestLabelMixin import RequestLabelMixin
from MSApi.mixin.GenListMixin import GenerateListMixin


class Assortment(ObjectMS,
                 GenerateListMixin,
                 RequestLabelMixin):
    _type_name = 'assortment'

    @classmethod
    @caching
    def gen_customtemplates(cls, **kwargs):
        return MSLowApi.gen_objects('entity/assortment/metadata/customtemplate', Template, **kwargs)
