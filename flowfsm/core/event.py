class EventRegistry:
    """Registry to manage dynamically created events."""
    _events = {}

    @classmethod
    def register(cls, name, terminal_states=None):
        """Register events and optionally define terminal states."""
        if name in cls._events:
            raise ValueError(f"Event '{name}' is already registered.")
        
        def create_event_class(name, terminal_states):
            """Dynamically creates an event class with terminal states."""
            def __init__(self):
                self.transitions = []
                self.terminal_states = terminal_states or []  # Default to an empty list if no terminal states are provided

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
        
        # Create and register the event class with terminal states
        event_class = create_event_class(name, terminal_states)
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
    def __init__(self, name, terminal_states=None):
        self.name = name
        self.terminal_states = terminal_states
        self._event_class = EventRegistry.register(name, terminal_states)
        self._event_instance = self._event_class()

    def __getattr__(self, attr):
        """Delegate attribute access to the event instance."""
        return getattr(self._event_instance, attr)

    def __repr__(self):
        """Represent the event instance."""
        return repr(self._event_instance)
    