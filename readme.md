# Laser VIRON (Version 2.3)

## Overview

This application is designed to control a Laser VIRON system using a graphical user interface (GUI) built with Tkinter. It enables users to connect to the laser via Telnet, send commands, and record operational data.

## Features

- **Telnet Connection**: Connect to the laser using IP and port configuration.
- **Command Execution**: Send various commands to control the laser operations.
- **Data Logging**: Record laser data and operational logs.
- **Temperature Monitoring**: Monitor the internal and diode temperatures of the laser.
- **Sound Alerts**: Play sound alerts for specific operations.

## Requirements

- Python 3.x
- Tkinter
- Telnetlib
- Playsound
- Threading
- CSV
- Time
- OS

## Installation

1. Clone the repository or download the `laser-custom-2.py` file.
2. Install the required Python packages:

    ```bash
    pip install tkinter playsound
    ```

3. Run the script:

    ```bash
    python laser-custom-2.py
    ```

## Usage

1. **Set Telnet Connection**: Configure the IP address and port for the Telnet connection in the UI.
2. **Connect to Laser**: Click the "Login" button to establish the Telnet connection.
3. **Send Commands**: Use the provided buttons to send pre-defined commands or enter custom commands manually.
4. **Monitor Temperature**: Use the temperature buttons to check the internal and diode temperatures of the laser.
5. **Start/Stop Recording**: Use the "Record" button to start recording laser data and "Stop" button to stop recording.

## GUI Components

- **Connection Settings**: Input fields for IP address, port, and user login.
- **Terminal**: Display the Telnet connection status and received responses.
- **Control Panel**: Buttons for starting, stopping, and resetting the laser, along with emergency stop and recording controls.
- **Temperature Monitoring**: Buttons to fetch internal and diode temperatures.
- **Command Execution**: Input field for manual command entry and a button to send the command.
- **Warning Label**: Displays a warning message regarding potential bugs.

## Directory Structure

- **logs/**: Directory to store the log files.

## Notes

- Ensure the IP address and port are correctly configured to match the laser system.
- Use the laser with caution as the software may have bugs.
- Logs are saved in the `logs` directory with timestamps for reference.

## Contributing

If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
