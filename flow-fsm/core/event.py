class EventRegistry:
    """Registry to manage dynamically created events."""
    _events = {}

    @classmethod
    def register(cls, name):
        if name in cls._events:
            raise ValueError(f"Event '{name}' is already registered.")
        
        def create_event_class(name):
            """Dynamically creates an event class."""
            def __init__(self):
                self.transitions = []

            def add_transition(self, transition):
                self.transitions.append(transition)

            def trigger(self, current_state):
                for transition in self.transitions:
                    if transition.source == current_state and transition.is_valid():
                        return transition
                return None

            methods = {
                "__init__": __init__,
                "add_transition": add_transition,
                "trigger": trigger,
                "__repr__": lambda self: f"<Event: {name}>",
            }
            return type(name, (object,), methods)
        
        event_class = create_event_class(name)
        cls._events[name] = event_class
        return event_class

    @classmethod
    def get(cls, name):
        if name not in cls._events:
            raise ValueError(f"Event '{name}' is not registered.")
        return cls._events[name]


class Event:
    """User API for creating and managing events."""
    def __init__(self, name):
        self.name = name
        self._event_class = EventRegistry.register(name)
        self._event_instance = self._event_class()

    def __getattr__(self, attr):
        return getattr(self._event_instance, attr)

    def __repr__(self):
        return repr(self._event_instance)
