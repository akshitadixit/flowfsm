from ..flowfsm.config.parser import parse_fsm_config
from ..flowfsm.config.loader import load_fsm_from_config
from ..flowfsm.runtime.executor import Executor

# Load FSM configuration
config = parse_fsm_config("./config_example.yml")

# Create FSM
workflow = load_fsm_from_config(config)

# Execute FSM
executor = Executor(workflow)
executor.run()
