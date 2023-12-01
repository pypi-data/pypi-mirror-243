import inspect

import requests
from MSApi.ObjectMS import ObjectMS

from MSApi.MSLowApi import MSLowApi, error_handler

from MSApi.Meta import Meta
from MSApi.Organization import Organization
from MSApi.Template import Template
from MSApi.Product import Product
from MSApi.exceptions import *
import MSApi as MSApi_module


class MSApi(MSLowApi):

    @classmethod
    def get_object_type(cls, obj_type_name) -> type:
        for member in inspect.getmembers(MSApi_module):
            if type(member[1]) is not type:
                continue
            if not issubclass(member[1], ObjectMS):
                continue
            if not hasattr(member[1], "_type_name"):
                continue
            if member[1].get_typename() == obj_type_name:
                return member[1]
        raise MSApiException("Object type \"{}\" not found".format(obj_type_name))

    @classmethod
    def get_object_by_json(cls, json_data):
        meta = Meta(json_data.get('meta'))
        return cls.get_object_type(meta.get_type())

    @classmethod
    def get_object_by_meta(cls, meta: Meta):
        return cls.get_object_type(meta.get_type())({'meta': meta.get_json()})

    @classmethod
    def get_object_by_href(cls, href):
        response = cls._auch_get_by_href(href)
        error_handler(response)
        return cls.get_object_by_json(response.json())

    @classmethod
    def load_label(cls, product: Product, organization: Organization, template: Template, sale_price=None, **kwargs):

        if not sale_price:
            sale_price = next(product.gen_sale_prices(), None)
            if not sale_price:
                raise MSApiException(f"Sale prices is empty in {product}")

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

        response = cls.auch_post(f"/entity/product/{product.get_id()}/export", json=request_json, **kwargs)
        if response.status_code == 303:
            url = response.json().get('Location')
            file_response = requests.get(url)
            data = file_response.content
        elif response.status_code == 200:
            data = response.content
        else:
            raise MSApiHttpException(response)

        return data
