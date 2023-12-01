from typing import Optional

from MSApi.MSLowApi import MSLowApi, error_handler
from MSApi.State import State
from MSApi.ObjectMS import check_init


class StateMixin:

    @classmethod
    def gen_states_list(cls, **kwargs):
        response = MSLowApi.auch_get("entity/{}/metadata".format(cls._type_name), **kwargs)
        error_handler(response)
        for states_json in response.json()["states"]:
            yield State(states_json)

    @check_init
    def get_state(self) -> Optional[State]:
        result = self._json.get('state')
        if result is not None:
            return State(result)
        return None
