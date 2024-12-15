import logging


class Logger:
    """Logging utility for FSM events and transitions."""

    @staticmethod
    def setup_logger():
        """Setup logger configuration."""
        logger = logging.getLogger("FSMLogger")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def log_event(event):
        logger = Logger.setup_logger()
        logger.info(f"Event triggered: {event.name}")

    @staticmethod
    def log_transition(transition):
        logger = Logger.setup_logger()
        logger.info(f"Transition from {transition.source} to {transition.target}")
