class FSMError(Exception):
    """Base class for FSM-related exceptions."""

    pass


class StateNotFoundError(FSMError):
    """Raised when a state is not found."""

    pass


class InvalidTransitionError(FSMError):
    """Raised when a transition is invalid."""

    pass
