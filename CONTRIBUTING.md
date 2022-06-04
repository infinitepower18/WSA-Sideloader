Whether it's a bug fix or a new feature, contributions to the project are always welcome! To get started, make sure you have [Python 3.10](https://www.python.org/downloads/windows/) and [Git](https://gitforwindows.org/) installed. Then clone this repo and install the required packages using `pip install -r requirements.txt`.

Please test the program before making your pull request. Starting from version 1.3.0, WSA Sideloader is compiled into an executable file using Nuitka. It is then distributed on GitHub Releases and Microsoft Store via the Inno installer.

To compile from source, follow the below instructions:

1. Download the latest version of [Python 3.10 64 bit](https://www.python.org/downloads/windows/)
2. Install Nuitka via pip using the command `pip install nuitka`
3. Clone the repository, and install the required dependencies using the command `pip install -r requirements.txt` in the root directory.
4. In the root directory run the command `nuitka --standalone sideloader.py --enable-plugin=pyqt5 --enable-plugin=tk-inter --windows-disable-console`. This may take some time depending on your computer.
5. Copy the icon.ico file and adbfiles folder to the sideloader.dist folder.

As this program is a sideloading tool for Windows Subsystem for Android, please make sure you are running Windows 11 with WSA installed.
