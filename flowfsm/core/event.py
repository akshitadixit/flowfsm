class EventRegistry:
    """Registry to manage dynamically created events."""

    _events = {}

    @classmethod
    def register(cls, name, auto_trigger=False):
        """Register events"""
        if name in cls._events:
            raise ValueError(f"Event '{name}' is already registered.")

        def create_event_class(name):
            """Dynamically creates an event class with terminal states."""

            def __init__(self):
                self.transitions = []

            def add_transition(self, transition):
                if (
                    transition.source.name != transition.target.name
                    and transition.source.is_terminal
                ):
                    # Raise an error if the source state is terminal and source != target
                    raise ValueError(
                        f"Invalid transition: '{transition}' source state is terminal."
                    )
                self.transitions.append(transition)

            def trigger(self, current_state):
                for transition in self.transitions:
                    if transition.source == current_state:
                        if transition.is_valid(self):
                            return transition
                return None

            methods = {
                "__init__": __init__,
                "add_transition": add_transition,
                "trigger": trigger,
                "auto_trigger": auto_trigger,
                "__repr__": lambda self: f"<Event: {name}>",
            }
            return type(name, (object,), methods)

        # Create and register the event class with terminal states
        event_class = create_event_class(name)
        cls._events[name] = event_class
        return event_class

    @classmethod
    def get(cls, name):
        """Retrieve an event class by name."""
        if name not in cls._events:
            raise ValueError(f"Event '{name}' is not registered.")
        return cls._events[name]

    @classmethod
    def clear(cls):
        """Clear all registered events."""
        cls._events = {}


class Event:
    """User API for creating and managing events."""

    def __init__(self, name, auto_trigger=False):
        self.name = name
        self._event_class = EventRegistry.register(name, auto_trigger)
        self._event_instance = self._event_class()

    def __getattr__(self, attr):
        """Delegate attribute access to the event instance."""
        return getattr(self._event_instance, attr)

    def __repr__(self):
        """Represent the event instance."""
        return repr(self._event_instance)
