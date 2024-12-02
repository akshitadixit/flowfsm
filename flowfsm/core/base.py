from .errors import InvalidTransitionError
from .state import StateRegistry

class FSMBaseMeta(type):
    """Metaclass to dynamically inject FSM behavior."""
    def __new__(cls, name, bases, dct):
        if "trigger_event" not in dct:
            dct["trigger_event"] = cls.generate_trigger_event_method()
        if "set_initial_state" not in dct:
            dct["set_initial_state"] = cls.generate_set_initial_state_method()
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def generate_trigger_event_method():
        def trigger_event(self, event):
            transition = event.trigger(self, self.current_state)
            if transition:
                self.current_state().exit()
                transition.execute()
                self.current_state = StateRegistry.get(transition.target.name)()
                self.current_state.enter()
            else:
                raise InvalidTransitionError(f"No valid transition for event '{event}' from state '{self.current_state}'.")
        return trigger_event

    @staticmethod
    def generate_set_initial_state_method():
        def set_initial_state(self, state_name):
            self.current_state = StateRegistry.get(state_name)()
            self.current_state.enter()
        return set_initial_state


class FSMBase(metaclass=FSMBaseMeta):
    """Base class for FSMs with dynamic behavior."""
    def __init__(self, name):
        self.name = name
        self.current_state = None

    def __repr__(self):
        return f"<FSM: {self.name}, Current State: {self.current_state}>"
