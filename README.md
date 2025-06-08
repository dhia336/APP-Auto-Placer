# APP-Auto-Placer

A powerful Windows application that helps you automatically open and position multiple applications on your screen using their shortcuts. Perfect for setting up your workspace with a single click!

## Features

- 🚀 Open multiple applications simultaneously
- 📐 Precisely position windows on your screen
- 📏 Set custom window sizes
- 💾 Save and load window configurations
- 🎯 Visual position and size selector
- 🔄 Import/Export configurations
- 🎨 Modern and intuitive user interface

## Installation

1. Clone the repository:


2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Launch the application:
```bash
python main.py
```

2. Add applications:
   - Click "ADD APP" to add a new application
   - Select the application shortcut (.exe or .lnk file)
   - Use the "Select Position" button to visually position the window
   - Set the desired window size

3. Save your configuration:
   - Click "EXPORT" to save your current configuration
   - Choose a location to save the JSON file

4. Load a configuration:
   - Click "IMPORT" to load a previously saved configuration
   - Select your saved JSON file

5. Open all applications:
   - Click "OPEN ALL" to launch and position all configured applications

## Configuration Format

The application saves configurations in JSON format. Example:
```json
[
  {
    "shortcut_path": "C:\\Path\\To\\App.exe",
    "position": [100, 100],
    "size": [800, 600]
  }
]
```

## Requirements

- Windows 10 or later
- Python 3.7 or later
- Required Python packages (see requirements.txt)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI
- Uses [pywinauto](https://github.com/pywinauto/pywinauto) for window management
