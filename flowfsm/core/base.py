from .errors import FSMError, InvalidTransitionError
from .state import StateRegistry


class FSMBaseMeta(type):
    """Metaclass to dynamically inject FSM behavior."""

    def __new__(cls, name, bases, dct):
        if "trigger_event" not in dct:
            dct["trigger_event"] = cls.generate_trigger_event_method()
        if "set_initial_state" not in dct:
            dct["set_initial_state"] = cls.generate_set_initial_state_method()
        if "auto_trigger_event" not in dct:
            dct["auto_trigger_event"] = cls.auto_trigger_event()
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def generate_trigger_event_method():
        def trigger_event(self, event):
            transition = event.trigger(self, self.current_state)
            if transition:
                self.current_state().exit()
                transition.execute(self)
                self.current_state = StateRegistry.get(transition.target.name)
                # entering the new state would return 1 if it's a terminal state
                if self.current_state().enter():
                    return 1
            else:
                raise InvalidTransitionError(
                    f"No valid transition for event '{event}' from state '{self.current_state}'."
                )

        return trigger_event

    @staticmethod
    def generate_set_initial_state_method():
        def set_initial_state(self, state=None):
            if not state:
                for _ in self.states:
                    if self.states[_].is_initial:
                        state = self.states[_]
                        break
            self.current_state = state
            if not self.current_state:
                raise FSMError("Initial state not set.")

        return set_initial_state

    @staticmethod
    def auto_trigger_event():
        def get_auto_trigger_event(self):
            for event_name in self.events:
                if self.events[event_name].auto_trigger:
                    return event_name
            raise FSMError(f"No auto trigger event found for {self.name}")

        return get_auto_trigger_event


class FSMBase(metaclass=FSMBaseMeta):
    """Base class for FSMs with dynamic behavior."""

    def __init__(self, name, states=None, transitions=None, events=None):
        self.name = name
        self.states = states or []
        self.transitions = transitions or []
        self.events = events or {}

    def __repr__(self):
        return f"<FSM: {self.name}, Current State: {self.current_state}>"
