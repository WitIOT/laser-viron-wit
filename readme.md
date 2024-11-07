
# Laser Project - VIRON (Version 2.5 with Sound)

This project is focused on controlling and recording data from a laser system using the `laser-custom-3.py` script. The software includes a graphical interface that allows toggling data recording, handling laser trigger signals, and processing signals from a PMT detector.

## Features

- **Laser Trigger and Detection**: Interfaces with a laser that shoots into the atmosphere, with trigger signals sent to an oscilloscope on channel 1 and a PMT detector reading on channel 2.
- **Data Recording Toggle**: Allows users to toggle data recording to a CSV file with a setting button next to the Mute button in the interface.
  - Displays "Enable Record" when data recording is on and "Disable Record" when off.
  - Default status is set to `False` (recording disabled).
- **Telnet Command Interface**: Supports Telnet commands for laser configuration, with commands formatted as `$COMMAND`, e.g., `MANUAL`, `DFREQ`, `QSDELAY`, etc.
- **Wi-Fi Configuration**: Prioritizes connecting to Wi-Fi SSID 'T480' on startup, with AP mode (which creates 'iriv' hotspot) disabled on boot.

## Requirements

- **Python Version**: Python 3.12.7
- **Dependencies**: Required Python libraries are listed in `requirements.txt`.
  - Common dependencies might include libraries for Telnet communication, GUI management, and data handling.

## Installation

1. Clone this repository:
   ```bash
   git clone [your-repo-url]
   cd your-repo-directory
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the main script:
   ```bash
   python laser-custom-3.py
   ```
2. **GUI Options**:
   - **Enable/Disable Recording**: Use the "Enable Record" button to start/stop recording data to a CSV file.
   - **Mute/Unmute**: Toggle sound output using the Mute button.
3. **Telnet Commands**: Configure laser settings using Telnet commands directly from the interface.

## Configuration

- **Wi-Fi Priority**: To ensure connection to the 'T480' network, configure Wi-Fi settings as needed.
- **Telnet Parameters**: Customize Telnet commands and response handling in the `telnet_send` function, which manages command sequences and logs responses.

## Troubleshooting

- **Connection Issues**: Verify network settings if you face issues connecting to the laser system via Telnet.
- **Data Output**: Ensure correct CSV formatting by checking the data recording toggle and command responses.
  
## License

This project is licensed under [Your License].
