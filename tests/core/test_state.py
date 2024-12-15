import unittest
from flowfsm.core.state import StateRegistry, State
from flowfsm.core.errors import StateNotFoundError

class TestStateRegistry(unittest.TestCase):
    def setUp(self):
        StateRegistry.clear()

    def test_register_state(self):
        state_class = StateRegistry.register("state1", is_initial=True)
        self.assertIn("state1", StateRegistry._states)
        self.assertEqual(state_class.name, "state1")
        self.assertTrue(state_class.is_initial)

    def test_register_duplicate_state(self):
        StateRegistry.register("state1")
        with self.assertRaises(ValueError):
            StateRegistry.register("state1")

    def test_get_registered_state(self):
        StateRegistry.register("state1")
        state_class = StateRegistry.get("state1")
        self.assertEqual(state_class.name, "state1")

    def test_get_unregistered_state(self):
        with self.assertRaises(StateNotFoundError):
            StateRegistry.get("state1")

    def test_clear_states(self):
        StateRegistry.register("state1")
        StateRegistry.clear()
        self.assertNotIn("state1", StateRegistry._states)

class TestState(unittest.TestCase):
    def setUp(self):
        StateRegistry.clear()

    def test_state_initialization(self):
        state = State("state1", is_initial=True)
        self.assertEqual(state.name, "state1")
        self.assertTrue(state.is_initial)

    def test_state_enter_exit_methods(self):
        state = State("state1", on_enter="Entering state1", on_exit="Exiting state1")
        self.assertEqual(state.enter(), 0)
        self.assertEqual(state.exit(), 0)

    def test_state_terminal_behavior(self):
        state = State("state1", is_terminal=True)
        self.assertEqual(state.enter(), 1)

    def test_state_repr(self):
        state = State("state1")
        self.assertEqual(repr(state), "<State: state1>")

if __name__ == '__main__':
    unittest.main()