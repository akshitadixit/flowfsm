import unittest
from flowfsm.core.workflow import Workflow
from flowfsm.core.base import FSMError
from flowfsm.core.state import StateRegistry

class TestWorkflow(unittest.TestCase):
    def setUp(self):
        StateRegistry.clear()
        self.states = {
            "state1": StateRegistry.register("state1", is_initial=True),
            "state2": StateRegistry.register("state2"),
        }
        self.transitions = [
            MockTransition("state1", "state2")
        ]
        self.events = {
            "event1": MockEvent("event1", auto_trigger=True),
            "event2": MockEvent("event2", auto_trigger=False),
        }
        self.workflow = Workflow(name="test_workflow", states=self.states, transitions=self.transitions, events=self.events)

    def test_initial_state_set(self):
        self.assertEqual(self.workflow.current_state.name, "state1")

    def test_auto_trigger_event_found(self):
        auto_event = self.workflow.auto_trigger_event()
        self.assertEqual(auto_event, "event1")

    def test_auto_trigger_event_not_found(self):
        self.workflow.events["event1"].auto_trigger = False
        with self.assertRaises(FSMError) as context:
            self.workflow.auto_trigger_event()
        self.assertEqual(str(context.exception), "No auto trigger event found for test_workflow")

    def test_trigger_event_valid_transition(self):
        self.workflow.trigger_event(self.events["event1"])
        self.assertEqual(self.workflow.current_state.name, "state2")

    def test_trigger_event_invalid_transition(self):
        with self.assertRaises(FSMError):
            self.workflow.trigger_event(self.events["event2"])

class MockState:
    def __init__(self, name, is_initial=False):
        self.name = name
        self.is_initial = is_initial
        
    def __call__(self):
        return self

    def enter(self):
        pass

    def exit(self):
        pass

class MockEvent:
    def __init__(self, name, auto_trigger=False):
        self.name = name
        self.auto_trigger = auto_trigger

    def trigger(self, fsm, current_state):
        if self.auto_trigger:
            return MockTransition("state1", "state2")
        return None

class MockTransition:
    def __init__(self, source_name, target_name):
        self.source = MockState(source_name)
        self.target = MockState(target_name)

    def execute(self, fsm):
        fsm.current_state = self.target

if __name__ == '__main__':
    unittest.main()