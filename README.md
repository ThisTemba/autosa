# Autosa

Autosa is Tenco software used to automate data acquisition using a signal analyzer (AUTOmated Signal Analysis or AUTOmatic Signal Analyzer). The name is spelled exactly as "Autosa" and is read as a single word with a stress on the second syllable.

## Getting Started

Windows is the recommended operating system for AutosaVersion 2022 Q3. It has not been tested on other operating systems.

### Autosa Installation

**Autosa has only been tested on Windows 10 and Windows 11 devices**

1. Download and Install [NI-VISA Version 2022 Q3](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html) for Windows. This allows Autosa to communicate with the instrument.
   1. This will download the NI package manager from which you will install NI-VISA
   2. Deselect all when it asks about additional packages, don't need those
2. Download the executable file [`Autosa.exe`](https://github.com/ThisTemba/autosa/blob/master/install/dist/Autosa.exe) from this repository
   1. Autosa is not a "recognized" windows app, so you may get a warning about that, ignore the warning and run the executable. You may have to click "More Info" and then "Run Anyway" to get it to run.
3. Double click the executable file to run the program

### Instrument Setup

1. Make sure the instrument is plugged in to power and turned on
2. Make sure the instrument is connected to this computer via USB-B (back of instrument) to USB-A (computer) cable. See image below.
3. Make sure the signal analyzer program is running on the device (called "LaunchXSA" on the desktop)


<img src="https://github.com/ThisTemba/autosa/assets/36087610/0b688734-af36-4af1-bae5-a3874f0893b7" width="300px" />

Required USB-B to USB-A cable



## Development

### Guiding Principles

This software is written to be as "plug-and-play" as possible. The more set up steps are required to use the software, the less likely it is to be used. This is why it comes packaged as an `.exe` file that just needs to be downloaded and double clicked. In this vein, all user interfaces should be as self-explanatory as possible.

Different levels of automation are available for differing comfort levels and use-cases. The most automated mode performs up to 5 runs in a row with no intervention. This is good for surveys, when everything is set up correctly and the procedure is merely repeated at each site. The least automated mode functions almost as an extension of the instrument's physical interface, allowing the user to start, stop, and save data manually. This is good for railcar EMC tests where timing varies and tests are repeated depending on the results.

### Packages

The following packages are required for development:

- [pysimplegui](https://www.pysimplegui.org/en/latest/) - creating user interface
- [pyinstaller](https://pyinstaller.org/en/stable/) - compiling python scripts `.exe` file
- [pyvisa](https://pyvisa.readthedocs.io/en/latest/) - communicating with the instrument over USB

Install all three with pip:

```bash
pip install pysimplegui pyinstaller pyvisa
```

### Building

This project uses [PyInstaller](https://pyinstaller.org/en/stable/) to convert the python scripts and packages into a single, distributable `.exe` file.

The build is done by executing the `build.py` file. The output executable (`.exe`) file will be located in `root/install/dist`. The `/install/build` folder are the temporary files used by PyInstaller to create the executable. I don't know what the `.spec` file is, but it doesn't seem to be required to run the executable.

## Real World Tests

### October 2023

Tenco used Autosa in the field for the first time on October 18th 2023 for railcar tests.
