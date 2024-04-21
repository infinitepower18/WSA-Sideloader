![GitHub release (latest by date)](https://img.shields.io/github/v/release/infinitepower18/wsa-sideloader)
![GitHub all releases](https://img.shields.io/github/downloads/infinitepower18/WSA-Sideloader/total?label=github%20downloads)
![Python](https://img.shields.io/badge/python-3.11-yellow)
![GitHub](https://img.shields.io/github/license/infinitepower18/wsa-sideloader)

# WSA Sideloader
WSA Sideloader is a tool that is used to easily install APK files on Windows Subsystem for Android. The program has been designed with simplicity and ease of use in mind.

You can also install XAPK, APKM and APKS files using this tool.

<img width="311" alt="image" src="https://github.com/infinitepower18/WSA-Sideloader/assets/44692189/8f0681b8-5597-4719-86d3-405e8d132722">

**Stay updated on the latest WSA Sideloader updates via the [WhatsApp](https://whatsapp.com/channel/0029VaCO0xB8kyySQFoGW12x) and [Telegram](https://t.me/WSASideloader) channels.**

## Download
Operating System|Source
|---------|---------|
|<img src="https://upload.wikimedia.org/wikipedia/commons/e/e6/Windows_11_logo.svg" style="width: 150px;"/>|[<img src="https://get.microsoft.com/images/en-US%20dark.svg" style="width: 200px;"/>](https://apps.microsoft.com/store/detail/9NMFSJB25QJR?cid=ghreadme&mode=direct)|
|<img src="https://upload.wikimedia.org/wikipedia/commons/e/e6/Windows_11_logo.svg" style="width: 150px;"/></br><img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Windows_10_Logo.svg" style="width: 150px;"/> |[<img src="https://user-images.githubusercontent.com/68516357/226141505-c93328f9-d6ae-4838-b080-85b073bfa1e0.png" style="width: 200px;"/>](https://github.com/infinitepower18/WSA-Sideloader/releases/latest)|
|<img src="https://upload.wikimedia.org/wikipedia/commons/e/e6/Windows_11_logo.svg" style="width: 150px;"/></br><img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Windows_10_Logo.svg" style="width: 150px;"/> |[<img src="https://user-images.githubusercontent.com/49786146/159123331-729ae9f2-4cf9-439b-8515-16a4ef991089.png" style="width: 200px;"/>](https://winstall.app/apps/infinitepower18.WSASideloader)|

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F1F1K06VY)
                
## Getting started

Make sure you have Windows Subsystem for Android installed on your machine. If you don't already have it, download it from [here](https://apps.microsoft.com/detail/9P3395VX91NR).

If you're not in a [supported country](https://support.microsoft.com/en-us/windows/countries-and-regions-that-support-amazon-appstore-on-windows-d8dd17c7-5994-4187-9527-ddb076f9493e), change your PC region setting to United States, you should then be able to download Amazon Appstore which contains the subsystem. You can change it back once you have installed it.

**Windows 10 users:** You can obtain community builds of WSA for Windows 10 from repositories like [WSABuilds](https://github.com/MustardChef/WSABuilds) and [WSAPatch](https://github.com/cinit/WSAPatch). Please note that the MS Store version of WSA Sideloader is not available on Windows 10. You can install it from the [releases page](https://github.com/infinitepower18/WSA-Sideloader/releases).

![image](https://user-images.githubusercontent.com/44692189/173249543-1a96679f-0773-4e41-8ddc-10e71ae189c2.png)

Enable developer mode in WSA settings. The subsystem will need to be running in order to install apps, however WSA Sideloader will attempt to start the subsystem for you if it's not running.

![image](https://user-images.githubusercontent.com/44692189/182655019-5cd310c6-8bbd-43b6-a60b-ebd35c12748c.png)

Choose the file you want to install and click the Install button. You can also install a file right from File Explorer, web browsers and other supported programs. You may need to authorize the ADB connection when using it for the first time.

You might see the below message if using WSA Sideloader for the first time. Just tick the box to always allow, allow the connection and run the installation again.

<img width="539" alt="image" src="https://github.com/infinitepower18/WSA-Sideloader/assets/44692189/b3e17d61-cd8e-4347-a674-4f738bc24fc1">

## Known issues
### APK installation failure in partially running mode
Microsoft has recently introduced a new partially running mode to WSA, and due to the way it works WSA Sideloader is not able to properly detect its running state and will show a "device offline" error should WSA enter its inactive state.

For now, you can open any app to wake up the subsystem before running WSA Sideloader. I hope to address this issue in a future update. Thank you for your patience.

## FAQ

### The APK installation fails with the error message "No connection could be made because the target machine actively refused it"
This is a [bug](https://github.com/microsoft/WSA/issues/136) with the subsystem itself, restarting the PC will usually fix it.

If you still get this error, try these steps:

1. Make sure WSA is turned off and disable WSA autostart in Task Manager, startup apps before proceeding with the below steps

2. Disable Hyper-V using the command `dism.exe /Online /Disable-Feature:Microsoft-Hyper-V` and reboot your PC

3. Reserve port 58526 so Hyper-V doesn't reserve it back using the command `netsh int ipv4 add excludedportrange protocol=tcp startport=58526 numberofports=1`

4. Re-enable Hyper-V using the command `dism.exe /Online /Enable-Feature:Microsoft-Hyper-V /All` and reboot your PC

### I installed the app successfully, but the app crashes while using it or doesn't work as intended.
WSA Sideloader is just an APK installer. Whether the app actually works or not depends on the app and the subsystem. Please be aware that apps that require Google Play Services may not work properly on WSA. You may try solutions such as [Magisk on WSA](https://github.com/LSPosed/MagiskOnWSALocal) if you want Google Play functionality.

You may check [this page](https://github.com/riverar/wsa-app-compatibility) for a list of compatible apps.

### What's the difference between downloading from GitHub and downloading from MS Store?
The Microsoft Store version is packaged as MSIX, allowing for clean installs/uninstalls as well as autoupdates. If you download the EXE installer from GitHub instead, you will have the option to install for yourself or for all users of the computer. The version that is in the winget package repository is the GitHub version.

It is recommended you download from Microsoft Store to ensure you get the latest features and bug fixes. Please note that the MS Store version is not available on Windows 10.

### Does Windows Subsystem for Android and WSA Sideloader work on my Windows VM running on my Apple Silicon Mac?
Due to lack of nested virtualization, running WSA on these systems is currently not possible.

### I would like to see [feature name] in your program. When can you implement it?
I am no longer accepting feature requests. Please see [this post](https://github.com/infinitepower18/WSA-Sideloader/discussions/112) for more information.

Bug reports will continue to be accepted.

### Where can I see a list of installed WSA apps?
You can press the "Installed apps" button to bring up a list of apps installed on the WSA. You can launch and uninstall apps through it as well as manage notifications, permissions etc. for each app. WSA apps are also present on the start menu and you can right click to uninstall just like any other Windows program.

If you would like to launch a list of installed apps right from the start menu, I have made an app for that. You can download it [here](https://github.com/infinitepower18/WSA-InstalledApps).

### How do I help translate WSA Sideloader into my language?
Thank you for your help! You may refer to [this readme](https://github.com/infinitepower18/WSA-Sideloader/blob/main/locales/README.md) for further details.

### What are some good places to download APK files from?
APKMirror and APKPure are two popular sites for downloading APK files.

## Support

Need help using WSA Sideloader? Post in the project's [discussions tab](https://github.com/infinitepower18/WSA-Sideloader/discussions). Found a bug? Visit the [issues page](https://github.com/infinitepower18/WSA-Sideloader/issues).

## Build Instructions

To compile from source, follow the below instructions:

1. Install [Git](https://gitforwindows.org/) if you haven't already. Then clone the repo using the command `git clone https://github.com/infinitepower18/WSA-Sideloader`
2. Download the latest version of [Python 3.11 64 bit](https://www.python.org/downloads/windows/). If you are compiling for ARM64, install the ARM64 version of Python 3.11 instead.
3. Install Nuitka via pip using the command `pip install nuitka`.
4. Install the required dependencies for WSA Sideloader using the command `pip install -r requirements.txt` in the root directory.
5. In the root directory run the command `nuitka --standalone sideloader.py --enable-plugin=tk-inter --windows-disable-console --windows-company-name=infinitepower18 --windows-product-name="WSA Sideloader" --windows-icon-from-ico=icon.ico --windows-product-version=<version> --windows-file-version=<version> --windows-file-description="WSA Sideloader"`. (replace `<version>` with the current version number) This may take some time depending on your computer.
6. Copy the icon.ico, apk.ico, aapt.exe files as well as the locales and platform-tools folders to the sideloader.dist folder.

## Privacy Policy

Please [click here](https://ahnafmahmud.com/apps/WSA-Sideloader/PrivacyPolicy.html) to view the privacy policy.

TLDR - No information is collected by this application.

## Disclaimer
This project is not affiliated with Microsoft or Google in any way.
