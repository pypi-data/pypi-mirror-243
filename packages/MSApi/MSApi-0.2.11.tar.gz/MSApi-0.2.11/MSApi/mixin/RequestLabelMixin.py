import requests

from MSApi.MSLowApi import MSLowApi

from MSApi.exceptions import MSApiException, MSApiHttpException
from MSApi.Template import Template
from MSApi.Organization import Organization
from MSApi.mixin.SalePricesMixin import SalePricesMixin, SalePrice


class RequestLabelMixin:

    def request_label(self, organization: Organization, template: Template, sale_price: SalePrice = None, **kwargs):
        if not sale_price:
            sale_price = next(self.gen_sale_prices(), None)
            if not sale_price:
                raise MSApiException(f"Sale prices is empty in {self}")

        request_json = {
            'organization': {
                'meta': organization.get_meta().get_json()
            },
            'count': 1,
            'salePrice': sale_price.get_json(),
            'template': {
                'meta': template.get_meta().get_json()
            }

        }

        response = MSLowApi.auch_post("entity/{}/{}/export".format(self._type_name, self.get_id()),
                                      json=request_json, **kwargs)
        if response.status_code == 303:
            url = response.json().get('Location')
            file_response = requests.get(url)
            data = file_response.content
        elif response.status_code == 200:
            data = response.content
        else:
            raise MSApiHttpException(response)
        return data
