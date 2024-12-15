from flowfsm.core.errors import FSMError


class Executor:
    """The executor runs the FSM based on events and transitions."""

    def __init__(self, workflows, in_parallel=False):
        self.workflows = workflows
        self.in_parallel = in_parallel

    def run(self):
        """Run the FSM, processing events and triggering transitions."""
        for name in self.workflows:
            print(f"-------------------------{name}-------------------------")
            workflow = self.workflows[name]
            if workflow.current_state().enter():
                raise FSMError("Initial state must not be a terminal state.")
            event_name = workflow.auto_trigger_event()
            while True:
                if event_name in workflow.events:
                    event = workflow.events[event_name]
                    if workflow.trigger_event(event):
                        print("FSM reached terminal state.")
                        break
                else:
                    print(f"Event '{event_name}' not found.")

                # get the next event from the user
                event_name = input("Enter the next event, leave empty to quit: ")
                if not event_name:
                    break
            print("-------------------------------------------------------------")
