from MSApi.ObjectMS import check_init


class ArchivedMixin:

    @check_init
    def is_archived(self):
        return bool(self._json.get('archived'))
