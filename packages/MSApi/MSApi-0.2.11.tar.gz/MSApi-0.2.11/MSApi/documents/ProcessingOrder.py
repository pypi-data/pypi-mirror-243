from typing import Optional
from datetime import datetime

from MSApi.ObjectMS import ObjectMS, check_init
from MSApi.MSLowApi import MSLowApi, error_handler, string_to_datetime, caching
from MSApi.State import State
from MSApi.Organization import Account
from MSApi.Project import Project
from MSApi.Attribute import Attribute
from MSApi.documents.Processing import Processing
from MSApi.documents.ProcessingPlan import ProcessingPlan

from MSApi.mixin.GenListMixin import GenerateListMixin
from MSApi.mixin.StateMixin import StateMixin
from MSApi.mixin.AccountIdMixin import AccountIdMixin
from MSApi.mixin.NameMixin import NameMixin
from MSApi.mixin.DescriptionMixin import DescriptionMixin
from MSApi.mixin.AttributeMixin import AttributeMixin


class ProcessingOrder(ObjectMS,
                      GenerateListMixin,
                      StateMixin,
                      AccountIdMixin,
                      NameMixin,
                      DescriptionMixin,
                      AttributeMixin):

    _type_name = 'processingorder'

    @check_init
    def get_sync_id(self) -> Optional[str]:
        return self._json.get('syncId')

    @check_init
    def get_updated_time(self) -> datetime:
        return string_to_datetime(self._json.get('updated'))

    @check_init
    def get_deleted_time(self) -> Optional[datetime]:
        return self._get_optional_object('deleted', string_to_datetime)

    @check_init
    def get_code(self) -> Optional[str]:
        return self._json.get('code')

    @check_init
    def get_external_code(self) -> Optional[str]:
        return self._json.get('externalCode')

    @check_init
    def get_moment_time(self) -> datetime:
        return string_to_datetime(self._json.get('moment'))

    @check_init
    def is_applicable(self) -> bool:
        return bool(self._json.get('applicable'))

    @check_init
    def get_project(self) -> Optional[Project]:
        return self._get_optional_object('project', Project)

    @check_init
    def get_organization_account(self) -> Optional[Account]:
        result = self._json.get('organizationAccount')
        if result is not None:
            return Account(result)
        return None

    @check_init
    def get_processing_plan(self) -> ProcessingPlan:
        return ProcessingPlan(self._json.get('processingPlan'))

    @check_init
    def get_quantity(self) -> int:
        return int(self._json.get('quantity'))

    @check_init
    def gen_processings(self):
        for attr in self._json.get('processings', []):
            yield Processing(attr)
