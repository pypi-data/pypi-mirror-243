from typing import Optional
from datetime import datetime

from MSApi.documents.DocumentMS import DocumentMS
from MSApi.MSLowApi import MSLowApi, error_handler, caching

from MSApi.mixin.GenListMixin import GenerateListMixin
from MSApi.mixin.CreateNewMixin import CreateNewMixin
from MSApi.mixin.NameMixin import NameMixin


class ProcessingPlan(DocumentMS,
                     GenerateListMixin,
                     CreateNewMixin,
                     NameMixin):

    _type_name = 'processingplan'

