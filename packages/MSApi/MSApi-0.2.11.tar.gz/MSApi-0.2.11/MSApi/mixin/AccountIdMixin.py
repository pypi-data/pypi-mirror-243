from MSApi.ObjectMS import check_init


class AccountIdMixin:

    @check_init
    def get_account_id(self):
        return self._json.get('accountId')
