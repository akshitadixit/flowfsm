class Executor:
    """The executor runs the FSM based on events and transitions."""
    def __init__(self, workflow):
        self.workflow = workflow

    def run(self):
        """Run the FSM, processing events and triggering transitions."""
        print(f"Starting FSM: {self.workflow.name}")
        while True:
            # Wait for events to trigger transitions
            event_name = "Activate" #input("Enter event name: ").strip()
            if event_name in self.workflow.events:
                event = self.workflow.events[event_name]
                self.workflow.trigger_event(event)
            else:
                print(f"Event '{event_name}' not found.")
