import unittest
from flowfsm.core.event import Event, EventRegistry

class MockState:
    def __init__(self, name, is_terminal=False):
        self.name = name
        self.is_terminal = is_terminal

class MockTransition:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def is_valid(self, event):
        return True

class TestEvent(unittest.TestCase):
    def setUp(self):
        EventRegistry.clear()
    
    def test_add_transition_valid(self):
        event = Event("TestEvent")
        source_state = MockState("source")
        target_state = MockState("target")
        transition = MockTransition(source_state, target_state)
        
        event.add_transition(transition)
        
        self.assertIn(transition, event.transitions)

    def test_add_transition_invalid_terminal_source(self):
        event = Event("TestEvent")
        source_state = MockState("source", is_terminal=True)
        target_state = MockState("target")
        transition = MockTransition(source_state, target_state)
        
        with self.assertRaises(ValueError) as context:
            event.add_transition(transition)
        
        self.assertIn("Invalid transition: '", str(context.exception))
        self.assertIn("source state is terminal.", str(context.exception))

    def test_add_transition_same_source_target_terminal(self):
        event = Event("TestEvent")
        source_state = MockState("state", is_terminal=True)
        target_state = MockState("state")
        transition = MockTransition(source_state, target_state)
        
        event.add_transition(transition)
        
        self.assertIn(transition, event.transitions)

    def test_add_transition_non_terminal_source(self):
        event = Event("TestEvent")
        source_state = MockState("source", is_terminal=False)
        target_state = MockState("target")
        transition = MockTransition(source_state, target_state)
        
        event.add_transition(transition)
        
        self.assertIn(transition, event.transitions)

if __name__ == '__main__':
    unittest.main()