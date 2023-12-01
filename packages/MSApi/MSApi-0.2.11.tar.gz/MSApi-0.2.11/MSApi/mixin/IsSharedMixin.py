from MSApi.ObjectMS import check_init


class IsSharedMixin:

    @check_init
    def is_shared(self) -> bool:
        return self._json.get('shared')
