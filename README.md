# Dev Board Finder

A script that helps to find connected development board usb-port name easily via the command line (Windows/Linux/Mac).
- Needs python 3  and pip to be executed.
## Installation
To install the script and set up the `dev-board-finder` command, just run the following one-liner in your terminal:

### Linux/macOS
```bash
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/DaniloCaruso/board-finder/main/installer.py)"
```

### Windows
For Windows users, you can run the following PowerShell command to download and install the script:
```bash
python -c "$(Invoke-WebRequest -Uri https://raw.githubusercontent.com/DaniloCaruso/board-finder/main/installer.py -UseBasicParsing).Content"
```


## Arguments

### Device Family
- ```-d, --device``` [optional]: Filter the search by specific development board families. 
    - Available options:
        - ```Arduino```
        - ```ESP```
        - ```Raspberry```
        - ```FTDI```
        - ```CH340```
        - ```CP210x```

#### Example:

```bash 
dev-board-finder -d Arduino ESP
```
This command will search only for Arduino and ESP devices.

### Enable Ports (macOS and Linux only)
On macOS and Linux, you can set the permissions for devices so you can access their serial ports.

- ```--enable-port, -ep``` [optional] : Set permissions for aall or a specific port (if not used at all, only port discovery is executed)


#### Enable all ports found:

```bash
dev-board-finder -ep
```

#### Enable a specific:

```bash
python3 dev-board-finder.py -ep ttyUSB0
```
Note: You may need sudo to set permissions.

### Help
You can always display the help message with the following command:

```bash
python3 dev-board-finder.py -h
```
## Example Output
After running the script, the detected devices will be listed:

```bash
🎉 Devices found:
  📌 /dev/ttyUSB0 - Family: Arduino
    📊 idVendor: 0x2341
    📊 idProduct: 0x0043
    ---
  📌 /dev/ttyUSB1 - Family: ESP
    📊 idVendor: 0x10C4
    📊 idProduct: 0xEA60
    ---
```
If no devices are found, the script will display:

```bash
😕 No devices found.
```

## Supported Platforms
- Linux: Tested on Ubuntu/Debian-based systems.
- macOS: Works on recent versions of macOS.
- Windows: Compatible with Windows 10 and later versions.

## Contributing
Feel free to submit issues and pull requests to improve the script or add new features!

## License
This project is licensed under the MIT License.

