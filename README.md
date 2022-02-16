![GitHub release (latest by date)](https://img.shields.io/github/v/release/infinitepower18/wsa-sideloader)
![GitHub all releases](https://img.shields.io/github/downloads/infinitepower18/wsa-sideloader/total)
![GitHub top language](https://img.shields.io/github/languages/top/infinitepower18/wsa-sideloader)
![GitHub](https://img.shields.io/github/license/infinitepower18/wsa-sideloader)

# WSA Sideloader
Easily sideload Android apps on Windows Subsystem for Android on Windows 11.

In order to use this program properly, make sure you enabled Developer mode in WSA settings and that WSA is running when using this.

![image](https://user-images.githubusercontent.com/44692189/154323024-3622e53d-5eeb-42ca-98ea-af6c51773daf.png)

[Download latest release](https://github.com/infinitepower18/WSA-Sideloader/releases/latest)

Currently, selecting "Install for anyone using this computer" during the install process is known to cause some issues. To avoid problems, please choose "Install just for me".

## Generating installer
Clone the repo, install [NSIS](https://nsis.sourceforge.io/Download) and [pynsist](https://pypi.org/project/pynsist/) and type `pynsist pynsist.cfg` to generate the installer.

Note that you need to [include some files](https://pynsist.readthedocs.io/en/latest/faq.html#packaging-with-tkinter) before it can generate.
