class TransitionRegistry:
    """Registry to manage dynamically created transitions."""
    _transitions = []

    @classmethod
    def register(cls, source, target, condition=None, action=None):
        def create_transition_class(source, target, condition=None, action=None):
            """Dynamically creates a transition class."""
            def is_valid(*args):
                return eval(condition) if condition else True

            def execute():
                if action:
                    eval(action)

            methods = {
                "is_valid": is_valid,
                "execute": execute,
                "__repr__": lambda self: f"<Transition: {source} -> {target}>",
                "source": source,
                "target": target,
                "condition": condition,
                "action": action,
            }
            return type(f"Transition_{source}_to_{target}", (object,), methods)
        
        transition_class = create_transition_class(source, target, condition, action)
        cls._transitions.append(transition_class)
        return transition_class

    @classmethod
    def get_all(cls):
        """Retrieve all registered transitions."""
        return cls._transitions
    
    @classmethod
    def clear(cls):
        """Clear all registered transitions."""
        cls._transitions = []


class Transition:
    """User API for creating transitions."""
    def __init__(self, source, target, condition=None, action=None):
        self._transition_class = TransitionRegistry.register(source, target, condition, action)
        self._transition_instance = self._transition_class()

    def __getattr__(self, attr):
        return getattr(self._transition_instance, attr)

    def __repr__(self):
        return repr(self._transition_instance)