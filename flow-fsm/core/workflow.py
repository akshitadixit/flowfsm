from .base import FSMBase
from .state import StateRegistry
from .transition import TransitionRegistry
from .event import EventRegistry


class Workflow(FSMBase):
    """Workflow class extending FSMBase."""
    def __init__(self, name, config):
        super().__init__(name)
        self.states = [StateRegistry.register(state) for state in config["states"]]
        self.transitions = [
            TransitionRegistry.register(
                src, tgt, condition=cfg.get("condition"), action=cfg.get("action")
            )
            for src, tgt, cfg in config["transitions"]
        ]
        self.events = {event: EventRegistry.register(event) for event in config["events"]}
