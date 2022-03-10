![GitHub release (latest by date)](https://img.shields.io/github/v/release/infinitepower18/wsa-sideloader)
![GitHub all releases](https://img.shields.io/github/downloads/infinitepower18/WSA-Sideloader/total?label=GitHub%20downloads)
![Uses Python 3.9.10](https://img.shields.io/badge/python-3.9.10-yellow)
![GitHub](https://img.shields.io/github/license/infinitepower18/wsa-sideloader)

# WSA Sideloader
Easily sideload Android apps on Windows Subsystem for Android on Windows 11.

![image](https://user-images.githubusercontent.com/44692189/157773590-898e2b39-40e9-4548-be39-f77605d9dfa4.png)

## Getting started

1. Make sure you have Windows Subsystem for Android installed on your Windows 11 machine. If you don't already have it, download it from [here](https://aka.ms/AmazonAppstore). You don't need to use the Amazon Appstore, however don't uninstall it as it will remove the subsystem.

2. Enable developer mode in WSA settings. It is also recommended you enable continuous mode, WSA Sideloader requires the subsystem to be running while sideloading apps.

![image](https://user-images.githubusercontent.com/44692189/154768380-f0b01ed7-e622-4fdd-8eb7-bf1c758f8103.png)

3. [Download the latest release of WSA Sideloader](https://github.com/infinitepower18/WSA-Sideloader/releases/latest). If you get a warning that the file might be unsafe, select keep anyway. The program is completely safe and the source code is available if you want to take a look at what it does. Alternatively, you can also download it from the [Microsoft Store](https://apps.microsoft.com/store/detail/wsa-sideloader/XP8K140DLVSC0L).

4. Choose the APK file you want to install and click the Install button. In most cases, you do not need to change the ADB address.

## FAQ

### I do not live in the US, how can I download the Windows Subsystem for Android?
Change your PC region setting to United States, you should then be able to download Amazon Appstore which contains the subsystem. You can change it back once you have installed it.

Amazon Appstore for WSA is currently not available outside the US, but when you have WSA Sideloader what's the need of the appstore? :)

### What's the difference between the GitHub version and Microsoft Store version?
Installing WSA Sideloader from the Microsoft Store is a one click install process. With the GitHub version, you have more control over your install, including installing for all users and changing the installation directory. The Microsoft Store version is installed at `C:\Users\[username]\AppData\Local\Programs\WSA Sideloader`.

Future updates will be published on both GitHub and Microsoft Store. You will get a message upon starting the program if an update is available. The GitHub version can be updated by downloading the latest version from the releases page while the MS Store version is updated via the Microsoft Store app.

There are no other differences between the two versions.

### Do you have a portable version?
Currently a portable version is not available.

### Can I use this tool to sideload apps on other Android devices?
This program has been designed with WSA in mind, however since it just automates all the ADB commands for you it should be possible to use it on other Android devices or emulators. You may need to change the ADB address for this and I cannot guarantee it will work properly on anything other than WSA.

### Can I install other kinds of apk files e.g. .xapk?
Currently only .apk files are supported.

### Where can I see a list of installed WSA apps?
You can press the "Installed apps" button to bring up a list of apps installed on the WSA. You can also launch and uninstall apps through it. WSA apps are also present on the start menu and you can right click to uninstall just like any other Windows program.

If you would like to launch a list of installed apps right from the start menu, I have made an app for that. You can download it [here](https://github.com/infinitepower18/WSA-InstalledApps).

### What's the best place to download APK files?
My personal recommendaton is [APKMirror](https://www.apkmirror.com/), it is run by Android Police founder Artem Russakovskii.

## Support

Need help using WSA Sideloader? Post in the project's [discussions tab](https://github.com/infinitepower18/WSA-Sideloader/discussions). Found a bug or want to make a feature request? Visit the [issues page](https://github.com/infinitepower18/WSA-Sideloader/issues).

## Disclaimer
This project is not affiliated with Microsoft or Google in any way.
