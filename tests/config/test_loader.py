import unittest
from flowfsm.config.loader import load_fsm_from_config
from flowfsm.core.state import StateRegistry
from flowfsm.core.transition import TransitionRegistry
from flowfsm.core.event import EventRegistry
from flowfsm.core.workflow import Workflow


class TestLoadFSMFromConfig(unittest.TestCase):
    def setUp(self):
        # Clear registries before each test
        StateRegistry.clear()
        TransitionRegistry.clear()
        EventRegistry.clear()

    def test_load_fsm_from_config_basic(self):
        config = {
            "workflows": [
                {
                    "name": "workflow1",
                    "states": {
                        "state1": {"is_initial": True},
                        "state2": {"is_terminal": True}
                    },
                    "transitions": [
                        {"source": "state1", "target": "state2"}
                    ],
                    "events": {
                        "event1": {
                            "transitions": [
                                {"source": "state1", "target": "state2"}
                            ]
                        }
                    }
                }
            ]
        }

        workflows = load_fsm_from_config(config)
        self.assertIn("workflow1", workflows)
        workflow = workflows["workflow1"]
        self.assertIsInstance(workflow, Workflow)
        self.assertIn("state1", workflow.states)
        self.assertIn("state2", workflow.states)
        self.assertEqual(len(workflow.transitions), 1)
        self.assertIn("event1", workflow.events)

    def test_load_fsm_from_config_multiple_workflows(self):
        config = {
            "workflows": [
                {
                    "name": "workflow1",
                    "states": {
                        "state1": {"is_initial": True},
                        "state2": {"is_terminal": True}
                    },
                    "transitions": [
                        {"source": "state1", "target": "state2"}
                    ],
                    "events": {
                        "event1": {
                            "transitions": [
                                {"source": "state1", "target": "state2"}
                            ]
                        }
                    }
                },
                {
                    "name": "workflow2",
                    "states": {
                        "state3": {"is_initial": True},
                        "state4": {"is_terminal": True}
                    },
                    "transitions": [
                        {"source": "state3", "target": "state4"}
                    ],
                    "events": {
                        "event2": {
                            "transitions": [
                                {"source": "state3", "target": "state4"}
                            ]
                        }
                    }
                }
            ]
        }

        workflows = load_fsm_from_config(config)
        self.assertIn("workflow1", workflows)
        self.assertIn("workflow2", workflows)

    def test_load_fsm_from_config_clear_registries(self):
        config1 = {
            "workflows": [
                {
                    "name": "workflow1",
                    "states": {
                        "state1": {"is_initial": True},
                        "state2": {"is_terminal": True}
                    },
                    "transitions": [
                        {"source": "state1", "target": "state2"}
                    ],
                    "events": {
                        "event1": {
                            "transitions": [
                                {"source": "state1", "target": "state2"}
                            ]
                        }
                    }
                }
            ]
        }

        config2 = {
            "workflows": [
                {
                    "name": "workflow2",
                    "states": {
                        "state3": {"is_initial": True},
                        "state4": {"is_terminal": True}
                    },
                    "transitions": [
                        {"source": "state3", "target": "state4"}
                    ],
                    "events": {
                        "event2": {
                            "transitions": [
                                {"source": "state3", "target": "state4"}
                            ]
                        }
                    }
                }
            ]
        }

        workflows1 = load_fsm_from_config(config1)
        self.assertIn("workflow1", workflows1)
        self.assertNotIn("workflow2", workflows1)

        workflows2 = load_fsm_from_config(config2)
        self.assertIn("workflow2", workflows2)
        self.assertNotIn("workflow1", workflows2)

if __name__ == '__main__':
    unittest.main()