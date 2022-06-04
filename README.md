![GitHub release (latest by date)](https://img.shields.io/github/v/release/infinitepower18/wsa-sideloader)
![GitHub all releases](https://img.shields.io/github/downloads/infinitepower18/WSA-Sideloader/total?label=GitHub%20downloads)
![Uses Python 3.10.4](https://img.shields.io/badge/python-3.10.4-yellow)
![GitHub](https://img.shields.io/github/license/infinitepower18/wsa-sideloader)

# WSA Sideloader
Easily sideload Android apps on Windows Subsystem for Android on Windows 11.

![image](https://user-images.githubusercontent.com/44692189/165937751-baf5c32d-ee57-4568-a9f4-db8ab70215c0.png)

## Download

<p><a href="https://apps.microsoft.com/store/detail/wsa-sideloader/XP8K140DLVSC0L">
<img src="https://getbadgecdn.azureedge.net/images/English_L.png" width="216" height="78">
</a></p>

Also available on [GitHub Releases](https://github.com/infinitepower18/WSA-Sideloader/releases).
                
## Getting started

1. Make sure you have Windows Subsystem for Android installed on your Windows 11 machine. If you don't already have it, download it from [here](https://aka.ms/AmazonAppstore). You don't need to use the Amazon Appstore, however don't uninstall it as it will remove the subsystem.

2. Enable developer mode in WSA settings. It is also recommended you enable continuous mode, however WSA Sideloader will attempt to start the subsystem for you if it's not running.

![image](https://user-images.githubusercontent.com/44692189/154768380-f0b01ed7-e622-4fdd-8eb7-bf1c758f8103.png)

3. Choose the APK file you want to install and click the Install button. In most cases, you do not need to change the ADB address.

## Planned updates

### .apk file association
I am happy to announce the implementation of this feature is now complete and working! I will run some final tests over the next few days before releasing version 1.3 which will include .apk file association.

## Known issues

### Text not clear depending on display scaling settings
DPI awareness is temporarily disabled due to a visual bug. I hope to fix this issue in a future update.

### No new ARM64 builds
No new builds will be released until further notice. More details can be found [here](https://github.com/infinitepower18/WSA-Sideloader/discussions/30).

## FAQ

### I do not live in the US, how can I download the Windows Subsystem for Android?
Change your PC region setting to United States, you should then be able to download Amazon Appstore which contains the subsystem. You can change it back once you have installed it.

Amazon Appstore for WSA is currently not available outside the US, but Microsoft plans to make the appstore and WSA available in France, Germany, UK, Italy and Japan by the end of this year.

### Why does it take so long for new updates to be released on Microsoft Store?
As much as I want the updates released on GitHub and Microsoft Store at the same time, this is something beyond my control. Sometimes they take up to 24 hours to approve the update, sometimes few days. There's nothing I can do about it unfortunately.

### I would like to see [feature name] in your program. When can you implement it?
I am open to suggestions and will try my best to add more relevant features to the program over time. If you have any suggestions you can open an issue with your suggestion. I usually fix bugs and maintain stability of the program before adding more stuff to it so it may take some time.

### Where can I see a list of installed WSA apps?
You can press the "Installed apps" button to bring up a list of apps installed on the WSA. You can launch and uninstall apps through it as well as manage notifications, permissions etc. for each app. WSA apps are also present on the start menu and you can right click to uninstall just like any other Windows program.

If you would like to launch a list of installed apps right from the start menu, I have made an app for that. You can download it [here](https://github.com/infinitepower18/WSA-InstalledApps).

### What's the best place to download APK files?
My personal recommendaton is [APKMirror](https://www.apkmirror.com/), it is run by Android Police founder Artem Russakovskii.

### I get an error when installing from Microsoft Store.
Please try installing from [GitHub releases](https://github.com/infinitepower18/WSA-Sideloader/releases/latest). If the installation still fails please post in [discussions](https://github.com/infinitepower18/WSA-Sideloader/discussions) for further assistance.

### The program does not uninstall properly.
Please make sure adb.exe is not running before uninstalling. If it is, stop it via Task Manager.

## Support

Need help using WSA Sideloader? Post in the project's [discussions tab](https://github.com/infinitepower18/WSA-Sideloader/discussions). Found a bug or want to make a feature request? Visit the [issues page](https://github.com/infinitepower18/WSA-Sideloader/issues).

For email support, [click here](https://forms.gle/Fkbyh7WRX17mQ7dW9).

## Privacy Policy

Please [click here](https://github.com/infinitepower18/WSA-Sideloader/blob/main/PrivacyPolicy.md) to view the privacy policy.

TLDR - No information is collected by this application.

## Contributing

Whether it's a bug fix or a new feature, contributions to the project are always welcome! To get started, make sure you have [Python 3.10](https://www.python.org/downloads/windows/) and [Git](https://gitforwindows.org/) installed. Then clone this repo and install the required packages using `pip install -r requirements.txt`.

Please test the program before making your pull request. This project uses Nuitka to build the executable file. Build instructions are available [here](https://github.com/infinitepower18/WSA-Sideloader/wiki/Build-Instructions).

As this program is a sideloading tool for Windows Subsystem for Android, please make sure you are running Windows 11 with WSA installed.

## Disclaimer
This project is not affiliated with Microsoft or Google in any way.
