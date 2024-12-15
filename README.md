# FlowFSM

## Project Overview

FlowFSM is a package for building and managing finite state machines (FSMs).  It provides tools for defining states, transitions, events, and workflows, simplifying the development of complex state-driven applications.  The framework will be supporting features for configuration, runtime management, and visualization as and when they are developed.

![](examples/screenshot.png)

## Features

* **Flexible State Definition:** Define states and transitions with ease using a clear and intuitive interface.
* **Event-Driven Transitions:** Trigger state transitions based on custom events.
* **Workflow Management:**  Manage complex workflows involving multiple states and transitions.
* **Configuration System:** Load configurations from various sources, enabling customization.
* **Runtime Execution:** Execute workflows and handle events efficiently.

## TODOs

* **Extensible Hooks and Listeners:** Extend functionality with custom hooks and listeners.
* **Visualization Support:**  Visualize workflows (future functionality, likely).
* **Robust Error Handling:**  Includes a comprehensive error handling system.


## Usage

A simple example showcasing 2 basic workflows can be found in the `examples/` directory.

```python

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

```