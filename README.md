![GitHub release (latest by date)](https://img.shields.io/github/v/release/infinitepower18/wsa-sideloader)
![MS Store downloads](https://img.shields.io/badge/ms%20store%20downloads-45k%2B-brightgreen)
![GitHub all releases](https://img.shields.io/github/downloads/infinitepower18/WSA-Sideloader/total?label=github%20downloads)
![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20ARM64-yellow)
![GitHub](https://img.shields.io/github/license/infinitepower18/wsa-sideloader)

# WSA Sideloader
WSA Sideloader is a tool that is used to easily install APK files on Windows Subsystem for Android. The program has been designed with simplicity and ease of use in mind.

![image](https://user-images.githubusercontent.com/44692189/172241903-a66b7d9f-0692-4178-81e4-561e3978ed9b.png)

## Download

<p><a href="https://www.microsoft.com/store/apps/9NMFSJB25QJR?cid=ghreadme">
<img src="https://user-images.githubusercontent.com/44692189/202488021-8670126b-e109-4ef7-ab98-3ee19396d71d.png" width="216" height="78">
</a></p>

You can also download from [GitHub Releases](https://github.com/infinitepower18/WSA-Sideloader/releases) or via winget using the command `winget install wsa-sideloader`
                
## Getting started

Make sure you have Windows Subsystem for Android installed on your Windows 11 machine. If you don't already have it, download it from [here](https://aka.ms/AmazonAppstore). You don't need to use the Amazon Appstore, however don't uninstall it as it will remove the subsystem.

If you're not in a [supported country](https://support.microsoft.com/en-us/windows/countries-and-regions-that-support-amazon-appstore-on-windows-d8dd17c7-5994-4187-9527-ddb076f9493e), change your PC region setting to United States, you should then be able to download Amazon Appstore which contains the subsystem. You can change it back once you have installed it.

![image](https://user-images.githubusercontent.com/44692189/173249543-1a96679f-0773-4e41-8ddc-10e71ae189c2.png)

Enable developer mode in WSA settings. The subsystem will need to be running in order to install apps, however WSA Sideloader will attempt to start the subsystem for you if it's not running.

![image](https://user-images.githubusercontent.com/44692189/182655019-5cd310c6-8bbd-43b6-a60b-ebd35c12748c.png)

Choose the APK file you want to install and click the Install button. In most cases, you do not need to change the ADB address. You can also install an APK file right from File Explorer, web browsers and other supported programs.

You might see the below message if using WSA Sideloader for the first time. Just tick the box to always allow, allow the connection and run the APK installation again.

<img width="327" alt="image" src="https://user-images.githubusercontent.com/44692189/195931968-3450beb9-895c-436b-8682-5b28727dc81a.png">

## Known issues

### No new ARM64 builds
No new builds have been released since version 1.1.10, however that will soon change as I now have current releases of WSA Sideloader running on ARM64. Expect a new ARM64 build shortly.

## FAQ

### I installed the app successfully, but the app crashes while using it or doesn't work as intended.
WSA Sideloader is just an APK installer. Whether the app actually works or not depends on the app and the subsystem. Please be aware that apps that require Google Play Services may not work properly on WSA. You may try solutions such as [Magisk on WSA](https://github.com/LSPosed/MagiskOnWSALocal) if you want Google Play functionality.

You may check [this page](https://github.com/riverar/wsa-app-compatibility) for a list of compatible apps.

### What's the difference between downloading from GitHub and downloading from MS Store?
The Microsoft Store version is packaged as MSIX, allowing for clean installs/uninstalls as well as autoupdates. If you download the EXE installer from GitHub instead, you will have the option to install for yourself or for all users of the computer.

It is recommended you download from Microsoft Store to ensure you get the latest features and bug fixes.

### I would like to see [feature name] in your program. When can you implement it?
I am open to suggestions and will try my best to add more relevant features to the program over time. If you have any suggestions you can open an issue with your suggestion. I usually fix bugs and maintain stability of the program before adding more stuff to it so it may take some time.

### Where can I see a list of installed WSA apps?
You can press the "Installed apps" button to bring up a list of apps installed on the WSA. You can launch and uninstall apps through it as well as manage notifications, permissions etc. for each app. WSA apps are also present on the start menu and you can right click to uninstall just like any other Windows program.

If you would like to launch a list of installed apps right from the start menu, I have made an app for that. You can download it [here](https://github.com/infinitepower18/WSA-InstalledApps).

### What are some good places to download APK files from?
APKMirror and APKPure are two popular sites for downloading APK files. Alternatively, you can install Aurora Store, an open source Play Store client.

## Support

Need help using WSA Sideloader? Post in the project's [discussions tab](https://github.com/infinitepower18/WSA-Sideloader/discussions). Found a bug or want to make a feature request? Visit the [issues page](https://github.com/infinitepower18/WSA-Sideloader/issues).

## Privacy Policy

Please [click here](https://ahnafmahmud.me/apps/WSA-Sideloader/PrivacyPolicy.html) to view the privacy policy.

TLDR - No information is collected by this application.

## Contributing

Please read [CONTRIBUTING.md](https://github.com/infinitepower18/WSA-Sideloader/blob/main/CONTRIBUTING.md) for more information.

## Disclaimer
This project is not affiliated with Microsoft or Google in any way.
