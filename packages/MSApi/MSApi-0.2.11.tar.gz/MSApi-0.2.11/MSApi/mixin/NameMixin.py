from MSApi.ObjectMS import check_init


class NameMixin:
    @check_init
    def get_name(self):
        return self._json.get('name')
