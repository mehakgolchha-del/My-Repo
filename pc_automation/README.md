"""PC Automation Documentation."""

# PC Automation Module

Automate PC tasks like opening/closing applications, file management, and system control.

## Features

- **Application Control**: Open and close applications
- **File Management**: List, copy, and delete files
- **Screenshots**: Capture screen images
- **System Info**: Get CPU, memory, and disk usage
- **Volume Control**: Adjust system volume
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Quick Start

```python
from pc_automation.automation import PCAutomation

automation = PCAutomation()

# Open an application
automation.open_application("chrome")

# Take a screenshot
automation.take_screenshot()

# Get system information
info = automation.get_system_info()
print(info)

# List files
files = automation.get_file_list("./documents", extension=".txt")
print(files)
```

## API Reference

### PCAutomation

- `open_application(app_name)`: Open an application
- `close_application(app_name)`: Close an application
- `take_screenshot(output_path)`: Take a screenshot
- `get_file_list(directory, extension)`: List files in directory
- `copy_file(source, destination)`: Copy a file
- `delete_file(file_path)`: Delete a file
- `get_system_info()`: Get CPU, memory, disk stats
- `control_volume(level)`: Set volume 0-100

## Platform-Specific Notes

### Windows
- Uses `os.startfile()` for application launching
- Uses `taskkill` for application termination
- Requires `pycaw` for volume control

### macOS
- Uses `open -a` for application launching
- Uses `pkill` for termination
- Native volume control support

### Linux
- Uses subprocess for application launching
- Uses `pkill` for termination
- ALSA or PulseAudio for volume control

## Installation

```bash
# Additional dependencies
pip install psutil pycaw  # Windows only for pycaw
```
