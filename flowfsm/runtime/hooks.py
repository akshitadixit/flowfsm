class Hooks:
    """Manage hooks for transitions."""

    @staticmethod
    def before_transition(transition):
        """Pre-transition hook."""
        print(f"Before transition from {transition.source} to {transition.target}")

    @staticmethod
    def after_transition(transition):
        """Post-transition hook."""
        print(f"After transition from {transition.source} to {transition.target}")

    @staticmethod
    def during_event(event):
        """Event hook."""
        print(f"During event {event.name}")
