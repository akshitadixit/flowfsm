import unittest
from flowfsm.core.transition import TransitionRegistry, global_context

class TestTransitionRegistry(unittest.TestCase):
    def setUp(self):
        TransitionRegistry.clear()
        global_context.set({})

    def test_register_transition_valid_condition(self):
        condition = "context.get('value') == 1"
        global_context.set({"value": 1})
        transition_class = TransitionRegistry.register("state1", "state2", condition)
        transition_instance = transition_class()
        
        self.assertTrue(transition_instance.is_valid())

    def test_register_transition_invalid_condition(self):
        condition = "context.get('value') == 1"
        global_context.set({"value": 2})
        transition_class = TransitionRegistry.register("state1", "state2", condition)
        transition_instance = transition_class()
        
        self.assertFalse(transition_instance.is_valid())

    def test_register_transition_execute_action(self):
        action = "context['value'] = 2"
        global_context.set({"value": 1})
        transition_class = TransitionRegistry.register("state1", "state2", action=action)
        transition_instance = transition_class()
        
        transition_instance.execute()
        self.assertEqual(global_context.get()["value"], 2)

    def test_register_transition_repr(self):
        transition_class = TransitionRegistry.register("state1", "state2")
        transition_instance = transition_class()
        
        self.assertEqual(repr(transition_instance), "<Transition: state1 -> state2>")

    def test_get_all_transitions(self):
        TransitionRegistry.register("state1", "state2")
        TransitionRegistry.register("state2", "state3")
        
        transitions = TransitionRegistry.get_all()
        self.assertEqual(len(transitions), 2)

    def test_clear_transitions(self):
        TransitionRegistry.register("state1", "state2")
        TransitionRegistry.clear()
        
        transitions = TransitionRegistry.get_all()
        self.assertEqual(len(transitions), 0)

if __name__ == '__main__':
    unittest.main()