
from MSApi.Assortment import Assortment
from MSApi.mixin.AttributeMixin import AttributeMixin
from MSApi.mixin.SalePricesMixin import SalePricesMixin
from MSApi.mixin.ProductfolderMixin import ProductfolderMixin
from MSApi.mixin.RequestByIdMixin import RequestByIdMixin
from MSApi.mixin.GenListMixin import GenerateListMixin
from MSApi.mixin.NameMixin import NameMixin
from MSApi.mixin.AccountIdMixin import AccountIdMixin
from MSApi.mixin.DescriptionMixin import DescriptionMixin
from MSApi.mixin.ArchivedMixin import ArchivedMixin


class Service(Assortment,
              AttributeMixin,
              ProductfolderMixin,
              SalePricesMixin,
              RequestByIdMixin,
              GenerateListMixin,
              NameMixin,
              AccountIdMixin,
              DescriptionMixin,
              ArchivedMixin):

    _type_name = 'service'

# | **barcodes**            | Array(Object)                                             | Штрихкоды Комплекта. [Подробнее тут](../dictionaries/#suschnosti-usluga-uslugi-metadannye-uslug-shtrih-kody)                                                                                                                      |
# | **buyPrice**            | Object                                                    | Закупочная продажи. [Подробнее тут](../dictionaries/#suschnosti-usluga-uslugi-metadannye-uslug-zakupochnaq-cena)                                                                                                                  |
# | **code**                | String(255)                                               | Код Услуги                                                                                                                                                                                                                        |
# | **description**         | String(4096)                                              | Описание Услуги                                                                                                                                                                                                                   |
# | **discountProhibited**  | Boolean                                                   | Признак запрета скидок<br>`+Обязательное при ответе`                                                                                                                                                                              |
# | **effectiveVat**        | Int                                                       | Реальный НДС %<br>`+Только для чтения`                                                                                                                                                                                            |
# | **effectiveVatEnabled** | Boolean                                                   | Дополнительный признак для определения разграничения реального НДС = 0 или "без НДС". (effectiveVat = 0, effectiveVatEnabled = false) -> "без НДС", (effectiveVat = 0, effectiveVatEnabled = true) -> 0%.<br>`+Только для чтения` |
# | **externalCode**        | String(255)                                               | Внешний код Услуги<br>`+Обязательное при ответе`                                                                                                                                                                                  |
# | **files**               | MetaArray                                                 | Метаданные массива [Файлов](../dictionaries/#suschnosti-fajly) (Максимальное количество файлов - 100)<br>`+Expand`                                                                                                                |
# | **group**               | [Meta](../#mojsklad-json-api-obschie-swedeniq-metadannye) | Метаданные отдела сотрудника<br>`+Обязательное при ответе` `+Expand`                                                                                                                                                              |
# | **id**                  | UUID                                                      | ID Услуги<br>`+Обязательное при ответе` `+Только для чтения`                                                                                                                                                                      |
# | **meta**                | [Meta](../#mojsklad-json-api-obschie-swedeniq-metadannye) | Метаданные Услуги<br>`+Обязательное при ответе`                                                                                                                                                                                   |
# | **minPrice**            | Object                                                    | Минимальная цена. [Подробнее тут](../dictionaries/#suschnosti-usluga-uslugi-metadannye-uslug-minimal-naq-cena)                                                                                                                    |
# | **name**                | String(255)                                               | Наименование Услуги<br>`+Обязательное при ответе` `+Необходимо при создании`                                                                                                                                                      |
# | **owner**               | [Meta](../#mojsklad-json-api-obschie-swedeniq-metadannye) | Метаданные владельца (Сотрудника)<br>`+Expand`                                                                                                                                                                                    |
# | **pathName**            | String                                                    | Наименование группы, в которую входит Услуга<br>`+Обязательное при ответе` `+Только для чтения`                                                                                                                                   |
# | **paymentItemType**     | Enum                                                      | Признак предмета расчета. [Подробнее тут](../dictionaries/#suschnosti-usluga-uslugi-atributy-suschnosti-priznak-predmeta-rascheta)                                                                                                |
# | **productFolder**       | [Meta](../#mojsklad-json-api-obschie-swedeniq-metadannye) | Метаданные группы Комплекта<br>`+Expand`                                                                                                                                                                                          |
# | **salePrices**          | Array(Object)                                             | Цены продажи. [Подробнее тут](../dictionaries/#suschnosti-usluga-uslugi-metadannye-uslug-ceny-prodazhi)                                                                                                                           |
# | **shared**              | Boolean                                                   | Общий доступ<br>`+Обязательное при ответе`                                                                                                                                                                                        |
# | **syncId**              | UUID                                                      | ID синхронизации<br>`+Только для чтения` `+Заполнение при создании`                                                                                                                                                               |
# | **taxSystem**           | Enum                                                      | Код системы налогообложения. [Подробнее тут](../dictionaries/#suschnosti-usluga-uslugi-atributy-suschnosti-kod-sistemy-nalogooblozheniq)                                                                                          |
# | **uom**                 | [Meta](../#mojsklad-json-api-obschie-swedeniq-metadannye) | Единицы измерения<br>`+Expand`                                                                                                                                                                                                    |
# | **updated**             | DateTime                                                  | Момент последнего обновления сущности<br>`+Обязательное при ответе` `+Только для чтения`                                                                                                                                          |
# | **useParentVat**        | Boolean                                                   | Используется ли ставка НДС родительской группы. Если true для единицы ассортимента будет применена ставка, установленная для родительской группы.<br>`+Обязательное при ответе`                                                   |
# | **vat**                 | Int                                                       | НДС %                                                                                                                                                                                                                             |
# | **vatEnabled**          | Boolean                                                   | Включен ли НДС для услуги. С помощью этого флага для услуги можно выставлять НДС = 0 или НДС = "без НДС". (vat = 0, vatEnabled = false) -> vat = "без НДС", (vat = 0, vatEnabled = true) -> vat = 0%.                             |
