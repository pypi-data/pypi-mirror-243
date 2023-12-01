from typing import Optional
from datetime import datetime

from MSApi.ObjectMS import ObjectMS, check_init
from MSApi.MSLowApi import string_to_datetime
from MSApi.Organization import Account
from MSApi.Project import Project
from MSApi.Counterparty import Counterparty
import MSApi.documents
from MSApi.mixin.AttributeMixin import AttributeMixin
from MSApi.mixin.GenListMixin import GenerateListMixin
from MSApi.mixin.RequestByIdMixin import RequestByIdMixin
from MSApi.mixin.StateMixin import StateMixin


class CustomerOrder(ObjectMS,
                    AttributeMixin,
                    GenerateListMixin,
                    RequestByIdMixin,
                    StateMixin):

    _type_name = 'customerorder'

    def __init__(self, json):
        super().__init__(json)

    @check_init
    def get_account_id(self) -> str:
        return self._json.get('accountId')

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
    def get_name(self) -> str:
        return self._json.get('name')

    @check_init
    def get_description(self) -> Optional[str]:
        return self._json.get('description')

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
    def is_vat_enabled(self) -> bool:
        return bool(self._json.get('vatEnabled'))

    @check_init
    def is_vat_included(self) -> Optional[bool]:
        return self._get_optional_object('vatIncluded', bool)

    @check_init
    def get_agent(self) -> Optional[Counterparty]:
        return self._get_optional_object('agent', Counterparty)

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
    def gen_demands(self):
        for attr in self._json.get('demands', []):
            yield MSApi.documents.Demand(attr)

# sum	Int	Сумма Заказа в установленной валюте	Только для чтения	да	да	нет
# rate	Object	Валюта. Подробнее тут	—	да	да	нет
# owner	Meta	Владелец (Сотрудник)	—	да	нет	да
# shared	Boolean	Общий доступ	—	да	нет	нет
# group	Meta	Отдел сотрудника	—	да	нет	да
# organization	Meta	Метаданные юрлица	Необходимое при создании	да	да	да
#  ! agent	Meta	Метаданные контрагента	Необходимое при создании	да	да	да
# store	Meta	Метаданные склада	—	нет	да	да
# contract	Meta	Метаданные договора	—	нет	да	да
#  ! state	Meta	Метаданные статуса заказа	—	нет	да	да
# organizationAccount	Meta	Метаданные счета юрлица	—	нет	да	да
# agentAccount	Meta	Метаданные счета контрагента	—	нет	да	да
#  ! attributes	Array(Object)	Коллекция метаданных доп. полей. Поля объекта	—	нет	да	нет
# files	MetaArray	Метаданные массива Файлов (Максимальное количество файлов - 100)	—	да	нет	да
# created	DateTime	Дата создания	Только для чтения	да	да	нет
# printed	Boolean	Напечатан ли документ	Только для чтения	да	нет	нет
# published	Boolean	Опубликован ли документ	Только для чтения	да	нет	нет
# vatSum	Float	Сумма НДС	Только для чтения	да	да	нет
# positions	MetaArray	Метаданные позиций Заказа покупателя	—	да	да	да
# deliveryPlannedMoment	DateTime	Планируемая дата отгрузки	—	нет	да	нет
# payedSum	Float	Сумма входящих платежей по Заказу	Только для чтения	да	да	нет
# shippedSum	Float	Сумма отгруженного	Только для чтения	да	да	нет
# invoicedSum	Float	Сумма счетов покупателю	Только для чтения	да	да	нет
# reservedSum	Float	Сумма товаров в резерве	Только для чтения	да	да	нет
#  ! project	Meta	Метаданные проекта	—	нет	да	да
# taxSystem	Enum	Код системы налогообложения. Подробнее тут	—	нет	да	нет
# shipmentAddress	String(255)	Адрес доставки Заказа покупателя	—	нет	да	нет
# shipmentAddressFull	Object	Адрес доставки Заказа покупателя с детализацией по отдельным полям. Подробнее тут	—	нет	да	нет