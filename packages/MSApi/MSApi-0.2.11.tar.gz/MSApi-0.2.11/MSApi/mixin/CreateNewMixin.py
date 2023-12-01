from MSApi.MSLowApi import MSLowApi, error_handler


class CreateNewMixin:

    def create_new(self, **kwargs):
        response = MSLowApi.auch_post('entity/{}'.format(self._type_name), json=self.get_json(), **kwargs)
        error_handler(response)
        self.set_json(response.json())
