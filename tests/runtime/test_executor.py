import unittest
from unittest.mock import MagicMock, patch
from flowfsm.runtime.executor import Executor
from flowfsm.core.errors import FSMError

class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.workflow_mock = MagicMock()
        self.workflow_mock.current_state.return_value.enter.return_value = False
        self.workflow_mock.auto_trigger_event.return_value = "event1"
        self.workflow_mock.events = {"event1": MagicMock()}
        self.workflow_mock.trigger_event.return_value = False
        self.workflows = {"workflow1": self.workflow_mock}
        self.executor = Executor(self.workflows)

    @patch('builtins.print')
    def test_run_initial_state_terminal(self, mock_print):
        self.workflow_mock.current_state.return_value.enter.return_value = True
        with self.assertRaises(FSMError):
            self.executor.run()

    @patch('builtins.input', side_effect=["event1", ""])
    @patch('builtins.print')
    def test_run_event_found(self, mock_print, mock_input):
        self.workflow_mock.trigger_event.return_value = True  # Ensure FSM reaches terminal state
        self.executor.run()
        self.workflow_mock.trigger_event.assert_called_with(self.workflow_mock.events["event1"])
        mock_print.assert_any_call("FSM reached terminal state.")

    @patch('builtins.input', side_effect=["event2", ""])
    @patch('builtins.print')
    def test_run_event_not_found(self, mock_print, mock_input):
        self.executor.run()
        mock_print.assert_any_call("Event 'event2' not found.")
        
    @patch('builtins.input', side_effect=["event1", "event1", ""])
    @patch('builtins.print')
    def test_run_multiple_events(self, mock_print, mock_input):
        self.workflow_mock.trigger_event.side_effect = [False, True]  # First event doesn't reach terminal
        self.executor.run()
        self.assertEqual(self.workflow_mock.trigger_event.call_count, 2)
        mock_print.assert_any_call("FSM reached terminal state.")


    @patch('builtins.input', side_effect=[""])
    @patch('builtins.print')
    def test_run_no_event_entered(self, mock_print, mock_input):
        self.executor.run()
        mock_print.assert_any_call("-------------------------------------------------------------")

if __name__ == '__main__':
    unittest.main()