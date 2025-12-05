# Logging

Python scripts should use the built-in `logging` module for logging messages. This allows for better control over log levels, formatting, and output destinations.

## Basic Setup
```python
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
```

## Log Levels
Use appropriate log levels for different types of messages:
- `DEBUG`: Detailed information, typically of interest only when diagnosing problems.
- `INFO`: Confirmation that things are working as expected.
- `WARNING`: An indication that something unexpected happened, or indicative of some problem in the near future (e.g., ‘disk space low’). The software is still working as expected.
- `ERROR`: Due to a more serious problem, the software has not been able to perform some function.
- `CRITICAL`: A very serious error, indicating that the program itself may be unable to continue running.

