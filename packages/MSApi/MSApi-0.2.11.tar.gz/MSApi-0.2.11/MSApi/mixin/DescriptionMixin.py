from MSApi.ObjectMS import check_init


class DescriptionMixin:

    @check_init
    def get_description(self):
        return self._json.get('description')
