from .base import FSMBase


class Workflow(FSMBase):
    """Workflow class extending FSMBase."""

    def __init__(self, name, states, transitions, events):
        super().__init__(name, states, transitions, events)

        self.set_initial_state()
