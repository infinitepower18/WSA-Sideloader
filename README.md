![GitHub release (latest by date)](https://img.shields.io/github/v/release/infinitepower18/wsa-sideloader)
![GitHub all releases](https://img.shields.io/github/downloads/infinitepower18/WSA-Sideloader/total?label=GitHub%20downloads)
![PyPI - Downloads](https://img.shields.io/pypi/dm/WSA-Sideloader?label=PyPi%20downloads)
![Uses Python 3.10.4](https://img.shields.io/badge/python-3.10.4-yellow)
![GitHub](https://img.shields.io/github/license/infinitepower18/wsa-sideloader)

# WSA Sideloader
Easily sideload Android apps on Windows Subsystem for Android on Windows 11.

![image](https://user-images.githubusercontent.com/44692189/161448857-e50aceab-002c-46cb-a592-c1af1be83ac5.png)

## Getting started

1. Make sure you have Windows Subsystem for Android installed on your Windows 11 machine. If you don't already have it, download it from [here](https://aka.ms/AmazonAppstore). You don't need to use the Amazon Appstore, however don't uninstall it as it will remove the subsystem.

2. Enable developer mode in WSA settings. It is also recommended you enable continuous mode, WSA Sideloader requires the subsystem to be running while sideloading apps.

![image](https://user-images.githubusercontent.com/44692189/154768380-f0b01ed7-e622-4fdd-8eb7-bf1c758f8103.png)

3. Download the latest release of WSA Sideloader. You can download it from either [GitHub releases](https://github.com/infinitepower18/WSA-Sideloader/releases/latest) or [Microsoft Store](https://apps.microsoft.com/store/detail/wsa-sideloader/XP8K140DLVSC0L). If you already have Python 3.10 or 3.9 installed, you can download WSA Sideloader from [PyPi](https://pypi.org/project/WSA-Sideloader/) instead. Simply run `pip install WSA-Sideloader` to install it, and `wsa-sideloader` to launch the application.

4. Choose the APK file you want to install and click the Install button. In most cases, you do not need to change the ADB address.

## FAQ

### I do not live in the US, how can I download the Windows Subsystem for Android?
Change your PC region setting to United States, you should then be able to download Amazon Appstore which contains the subsystem. You can change it back once you have installed it.

Amazon Appstore for WSA is currently not available outside the US, but when you have WSA Sideloader what's the need of the appstore? :)

### Why does it take so long for new updates to be released on Microsoft Store?
As much as I want the updates released on GitHub, PyPi and Microsoft Store at the same time, this is something beyond my control. Sometimes they take up to 24 hours to approve the update, sometimes few days. There's nothing I can do about it unfortunately.

### Can I use this tool to sideload apps on other Android devices?
This program has been designed with WSA in mind, however since it just automates all the ADB commands for you it should be possible to use it on other Android devices or emulators. You may need to change the ADB address for this and I cannot guarantee it will work properly on anything other than WSA.

### I would like to see [feature name] in your program. When can you implement it?
I am open to suggestions and will try my best to add more relevant features to the program over time. If you have any suggestions you can open an issue with your suggestion. I usually fix bugs and maintain stability of the program before adding more stuff to it so it may take some time.

### Where can I see a list of installed WSA apps?
You can press the "Installed apps" button to bring up a list of apps installed on the WSA. You can launch and uninstall apps through it as well as manage notifications, permissions etc. for each app. WSA apps are also present on the start menu and you can right click to uninstall just like any other Windows program.

If you would like to launch a list of installed apps right from the start menu, I have made an app for that. You can download it [here](https://github.com/infinitepower18/WSA-InstalledApps).

### What's the best place to download APK files?
My personal recommendaton is [APKMirror](https://www.apkmirror.com/), it is run by Android Police founder Artem Russakovskii.

### The program does not uninstall properly.
Please make sure adb.exe is not running before uninstalling. If it is, stop it via Task Manager.

## Support

Need help using WSA Sideloader? Post in the project's [discussions tab](https://github.com/infinitepower18/WSA-Sideloader/discussions). Found a bug or want to make a feature request? Visit the [issues page](https://github.com/infinitepower18/WSA-Sideloader/issues).

For email support, [click here](https://forms.gle/Fkbyh7WRX17mQ7dW9).

## Contributing

Whether it's a bug fix or a new feature, contributions to the project are always welcome! To get started, make sure you have [Python 3.10](https://www.python.org/downloads/windows/) and [Git](https://gitforwindows.org/) installed. Then clone this repo and install the required packages using `pip install -r requirements.txt`.

Please test the program before making your pull request. This project uses [pynsist](https://pynsist.readthedocs.io/en/latest/) to build the NSIS installer. You may want to build the installer and test the program by running it from the installer as that's how the application will be distributed to non Python users. However, you should ensure that the output path is set to `"$INSTDIR"` (after running pynsist, there will be an installer.nsi file located at build/nsis, you need to change line 137)

As this program is a sideloading tool for Windows Subsystem for Android, please make sure you are running Windows 11 with WSA installed.

## Disclaimer
This project is not affiliated with Microsoft or Google in any way.
