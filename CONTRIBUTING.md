Whether it's a bug fix or a new feature, contributions to the project are always welcome! To get started, make sure you have [Python 3.10](https://www.python.org/downloads/windows/) and [Git](https://gitforwindows.org/) installed. Then clone this repo and install the required packages using `pip install -r requirements.txt`.

Please test the program before making your pull request. This project uses [pynsist](https://pynsist.readthedocs.io/en/latest/) to build the NSIS installer. You may want to build the installer and test the program by running it from the installer as that's how the application will be distributed. However, you should ensure that the output path is set to `"$INSTDIR"` (after running pynsist, there will be an installer.nsi file located at build/nsis, you need to change line 134)

As this program is a sideloading tool for Windows Subsystem for Android, please make sure you are running Windows 11 with WSA installed.
