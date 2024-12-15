# State Registry to manage dynamically created state classes
from flowfsm.core.errors import StateNotFoundError


class StateRegistry:
    """Manages all dynamically created state classes."""

    _states = {}

    @classmethod
    def register(
        cls, name, on_enter=None, on_exit=None, is_initial=False, is_terminal=False
    ):
        def create_state_class(
            name, on_enter=None, on_exit=None, is_initial=False, is_terminal=False
        ):
            """Dynamically creates a state class with custom behavior."""

            def enter(self):
                print(on_enter if on_enter else f"Entering {name}")
                if is_terminal:
                    self.exit()
                    return 1
                return 0

            def exit(self):
                print(on_exit if on_exit else f"Exiting {name}")
                return 0

            methods = {
                "enter": enter,
                "exit": exit,
                "__repr__": lambda self: f"<State: {name}>",
                "name": name,
                "on_enter": on_enter,
                "on_exit": on_exit,
                "is_initial": is_initial,
                "is_terminal": is_terminal,
            }
            return type(name, (object,), methods)

        if name in cls._states:
            raise ValueError(f"State '{name}' is already registered.")
        state_class = create_state_class(
            name, on_enter, on_exit, is_initial, is_terminal
        )
        cls._states[name] = state_class
        return state_class

    @classmethod
    def get(cls, name):
        """Retrieve a registered state class by name."""
        if name not in cls._states:
            raise StateNotFoundError(f"State '{name}' is not registered.")
        return cls._states[name]

    @classmethod
    def clear(cls):
        """Clear all registered states."""
        cls._states = {}


# User-facing State API
class State:
    """User API for creating and using states."""

    def __init__(
        self, name, on_enter=None, on_exit=None, is_initial=False, is_terminal=False
    ):
        self.name = name
        self._state_class = StateRegistry.register(
            name, on_enter, on_exit, is_initial, is_terminal
        )
        self._state_instance = self._state_class()

    def __getattr__(self, attr):
        """Delegate attribute access to the dynamically created state instance."""
        return getattr(self._state_instance, attr)

    def __repr__(self):
        return repr(self._state_instance)
