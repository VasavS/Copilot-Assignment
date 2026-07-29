# Copilot-Assignment

## 1. What code did Github Copilot generate?
Github copilot generated a Python script named `copilot_test.py` that displays the system uptime in a human-readable format. The script is designed to work across multiple operating systems by using different methods to retrieve the system boot time.

## 2. Modifications made in the script:
Minor modifications were made to improve the quality and reliability of the generated code.

The changes included:
- Reviewing and refining the exception handling to ensure the program fails gracefully when a particular uptime retrieval method is unavailable.
- Improving code readability by organizing the logic into separate functions (`format_uptime()`, `get_uptime_seconds()`, and `main()`).
- Adding comments throughout the script to make the implementation easier to understand and maintain.
- Verifying that platform-specific fallback methods execute in the correct order, ensuring the script remains portable across Linux, macOS, and Windows.

## 3. Testing the script:
The script was tested by executing it from the command line using Python.

### Test Procedure
1. Saved the generated script as `copilot_test.py`.
2. Opened a terminal in the project directory.
3. Executed the command:

```bash
python copilot_test.py
```

### Expected Result
The program successfully displayed the system uptime in a human-readable format, such as:

```
1 hours, 18 minutes, 12 seconds
```
