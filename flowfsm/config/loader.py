from ..core.workflow import Workflow
from ..core.state import StateRegistry
from ..core.transition import TransitionRegistry
from ..core.event import EventRegistry


def create_states(states_config):
    """Dynamically create states based on the configuration."""
    states = {}
    for state_name, state_config in states_config.items():
        on_enter, on_exit = state_config.get("on_enter"), state_config.get("on_exit")
        is_terminal, is_initial = (
            state_config.get("is_terminal", False),
            state_config.get("is_initial", False),
        )
        state = StateRegistry.register(
            state_name,
            on_enter=on_enter,
            on_exit=on_exit,
            is_initial=is_initial,
            is_terminal=is_terminal,
        )
        states[state_name] = state
    return states


def create_transitions(transitions_config):
    """Dynamically create transitions based on the configuration."""
    transitions = []
    for transition in transitions_config:
        source, target = (
            StateRegistry.get(transition["source"]),
            StateRegistry.get(transition["target"]),
        )
        condition, action = transition.get("condition"), transition.get("action")
        transition = TransitionRegistry.register(
            source, target, condition=condition, action=action
        )
        transitions.append(transition)
    return transitions


def create_events(events_config, transitions):
    """Dynamically create events and bind them to transitions."""
    events = {}
    for event_name, event_config in events_config.items():
        event = EventRegistry.register(
            event_name, event_config.get("auto_trigger", False)
        )
        for transition in event_config["transitions"]:
            # Find the transition object based on source and target
            for t in transitions:
                if (
                    t.source == transition["source"]
                    and t.target == transition["target"]
                ):
                    event.add_transition(t)
                    break
        events[event_name] = event
    return events


def load_fsm_from_config(config):
    """Create multiple workflows from the configuration file."""
    workflows = {}
    # Clear registries to avoid conflicts
    StateRegistry.clear()
    TransitionRegistry.clear()
    EventRegistry.clear()

    for workflow_config in config["workflows"]:
        workflow_name = workflow_config["name"]
        # Create states, transitions, and events for the current workflow
        states = create_states(workflow_config["states"])
        transitions = create_transitions(workflow_config["transitions"])
        events = create_events(workflow_config["events"], transitions)
        workflow = Workflow(workflow_name, states, transitions, events)
        workflows[workflow_name] = workflow

    return workflows
