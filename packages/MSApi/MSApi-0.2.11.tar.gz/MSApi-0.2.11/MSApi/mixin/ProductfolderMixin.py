from typing import Optional

from MSApi.ObjectMS import check_init
from MSApi.ProductFolder import ProductFolder


class ProductfolderMixin:

    @check_init
    def get_productfolder(self) -> Optional[ProductFolder]:
        """Группа"""
        result = self._json.get('productFolder')
        if result is None:
            return None
        return ProductFolder(result)
