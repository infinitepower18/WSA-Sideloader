![GitHub release (latest by date)](https://img.shields.io/github/v/release/infinitepower18/wsa-sideloader)
![GitHub all releases](https://img.shields.io/github/downloads/infinitepower18/wsa-sideloader/total)
![GitHub top language](https://img.shields.io/github/languages/top/infinitepower18/wsa-sideloader)
![GitHub](https://img.shields.io/github/license/infinitepower18/wsa-sideloader)

# WSA Sideloader
Easily sideload Android apps on Windows Subsystem for Android on Windows 11.

![image](https://user-images.githubusercontent.com/44692189/154756555-4eeb02a1-cc41-48a4-9577-1a6eea8aad87.png)

## Getting started

1. Make sure you have Windows Subsystem for Android installed on your Windows 11 machine. If you don't already have it, download it from [here](https://aka.ms/AmazonAppstore). You don't need to use the Amazon Appstore, however don't uninstall it as it will remove the subsystem.

2. Enable developer mode in WSA settings. It is also recommended you enable continuous mode, WSA Sideloader requires the subsystem to be running while sideloading apps.

![image](https://user-images.githubusercontent.com/44692189/154768380-f0b01ed7-e622-4fdd-8eb7-bf1c758f8103.png)

3. [Download the latest release of WSA Sideloader](https://github.com/infinitepower18/WSA-Sideloader/releases/latest). If you get a warning that the file might be unsafe, select keep anyway. The program is completely safe and the source code is available if you want to take a look at what it does.

4. After installing WSA Sideloader, you may need to download the SDK platform tools, as the program depends on it to do its magic. This is a one time process and the download size is about 11.5 MB.

5. Choose the APK file you want to install and click the Install button. In most cases, you do not need to change the ADB address.

## FAQ

### I do not live in the US, how can I download the Windows Subsystem for Android?
Change your PC region setting to United States, you should then be able to download Amazon Appstore which contains the subsystem. You can change it back once you have installed it.

Amazon Appstore for WSA is currently not available outside the US, but when you have WSA Sideloader what's the need of the appstore? :)

### Do you have a portable version?
Currently a portable version is not available.

### Can I use this tool to sideload apps on other Android devices?
This program has been designed with WSA in mind, however since it just automates all the ADB commands for you it should be possible to use it on other Android devices or emulators. You may need to change the ADB address for this and I cannot guarantee it will work properly on anything other than WSA.

### Can I install other kinds of apk files e.g. .xapk?
Currently only .apk files are supported.

### Where can I see a list of installed WSA apps?
You can press the "Installed apps" button to bring up a list of apps installed on the WSA. You can also launch and uninstall apps through it. WSA apps are also present on the start menu and you can right click to uninstall just like any other Windows program.

### What's the best place to download APK files?
My personal recommendaton is [APKMirror](https://www.apkmirror.com/), it is run by Android Police founder Artem Russakovskii.
