# CLI Interface Contract

## Command Format
All commands follow the format: `command [arguments]`

## Standard Commands

### help
- **Purpose**: Display available commands and their usage
- **Arguments**: None or specific command name
- **Output**: List of available commands or detailed help for a specific command
- **Error cases**: None

### exit
- **Purpose**: Terminate the application gracefully
- **Arguments**: None
- **Output**: None (application terminates)
- **Error cases**: None

## Command Response Format
- Success: Plain text response with requested information
- Error: "Error: [descriptive message]" followed by a newline
- Info: "Info: [informational message]" followed by a newline

## Input Validation
- Empty input: Display error message and prompt for valid input
- Invalid command: Display "Unknown command: [command_name]" and available commands
- Invalid arguments: Display specific error about argument requirements

## Exit Conditions
- User enters 'exit' command
- User presses Ctrl+C
- User presses Ctrl+D (EOF on Unix-like systems)