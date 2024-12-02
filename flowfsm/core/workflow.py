from .base import FSMBase
from .state import StateRegistry
from .transition import Transition
from .event import EventRegistry


class Workflow(FSMBase):
    """Workflow class extending FSMBase."""
    def __init__(self, name, states, transitions, events):
        super().__init__(name)
        
        self.states = states
        self.current_state = self.states[0][1]
        self.current_state().enter()
        self.transitions = transitions
        self.events = events
