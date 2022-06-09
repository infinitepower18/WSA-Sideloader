import os
import PySimpleGUI as gui
import platform
import webbrowser
import sys
import urllib
import urllib.error
from windows_toasts import WindowsToaster, ToastText3
import ctypes
from pkg_resources import parse_version
from button import RoundedButton
import darkdetect
from os.path import exists

# Block usage on non Windows OS
if(platform.system() != "Windows"):
    print("This operating system is not supported.")
    sys.exit(0)

ctypes.windll.shcore.SetProcessDpiAwareness(True) # Make program DPI aware
wintoaster = WindowsToaster('WSA Sideloader')

version = "1.3.0"

if darkdetect.isDark():
    gui.theme("LightGrey")
    gui.theme_background_color("#232020")
    gui.theme_text_element_background_color("#232020")
    gui.theme_text_color("White")
    gui.theme_button_color(('#232020', '#ADD8E6'))
    gui.theme_input_background_color('#ADD8E6')
    gui.theme_input_text_color('#000000')
else:
    gui.theme("LightGrey")

def startgit(filearg = ""):
    global installsource
    installsource = "GitHub (via git clone)"
    global explorerfile
    explorerfile = filearg
    
    # Check if OS is Windows 11
    if int(platform.win32_ver()[1].split('.')[2]) < 22000:
        layout = [[gui.Text('You need Windows 11 to use WSA Sideloader (as well as the subsystem itself). Please upgrade your operating system and install WSA before running this program.\nFor more information and support, visit the WSA Sideloader GitHub page.',font=("Calibri",11))],
                [RoundedButton("Exit",0.3,font="Calibri 11"),RoundedButton("GitHub",0.3,font="Calibri 11")]]
        window = gui.Window('Unsupported OS', layout,icon="icon.ico",debugger_enabled=False)

        event, values = window.Read()
        if event == "GitHub":
            window.Close()
            webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader/",2)
            sys.exit(0)
        elif event is None or "Exit":
            sys.exit(0)
        window.Close()
        
    main()
    
def startstore(filearg = ""): # For Microsoft Store installs
    global installsource
    installsource = "Microsoft Store"
    global explorerfile
    explorerfile = filearg
    try:
        file = urllib.request.urlopen("https://github.com/infinitepower18/WSA-Sideloader/raw/main/latestversion")
        lines = [line.decode("utf-8") for line in file]
        latestver = lines[1].rstrip()
        if parse_version(latestver) > parse_version(version):
            layout = [[gui.Text('A newer version of WSA Sideloader is available.\nVisit the Microsoft Store to download the latest version.',font=("Calibri",11))],
                [RoundedButton("Update now",0.3,font="Calibri 11"),RoundedButton("Later",0.3,font="Calibri 11")]]
            window = gui.Window('Update available', layout,icon="icon.ico",debugger_enabled=False)
            event, values = window.Read()
            if event is None:
                sys.exit(0)
            elif event == "Update now":
                window.Close()
                webbrowser.open("ms-windows-store://pdp/?productid=XP8K140DLVSC0L",2)
                sys.exit(0)
            elif event == "Later":
                window.Close()
                main()
        else:
            main()
    except (urllib.error.URLError,urllib.error.HTTPError,urllib.error.ContentTooShortError) as error: # Skip update check in case of network error
        main()

def start(filearg = ""): # For GitHub installs
    global installsource
    installsource = "GitHub"
    global explorerfile
    explorerfile = filearg
    try:
        file = urllib.request.urlopen("https://github.com/infinitepower18/WSA-Sideloader/raw/main/latestversion")
        lines = [line.decode("utf-8") for line in file]
        latestver = lines[0].rstrip()
        if parse_version(latestver) > parse_version(version):
            layout = [[gui.Text('A newer version of WSA Sideloader is available.\nWould you like to update now?',font=("Calibri",11))],
                [RoundedButton("Yes",0.3,font="Calibri 11"),RoundedButton("No",0.3,font="Calibri 11")]]
            window = gui.Window('Update available', layout,icon="icon.ico",debugger_enabled=False)
            event, values = window.Read()
            if event is None:
                sys.exit(0)
            elif event == "Yes":
                window.Close()
                webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader/releases/latest",2)
                sys.exit(0)
            elif event == "No":
                window.Close()
                main()
        else:
            main()
    except (urllib.error.URLError,urllib.error.HTTPError,urllib.error.ContentTooShortError) as error: # Skip update check in case of network error
        main()
    
def adbEmpty():
    adbEmptyToast = ToastText3()
    adbEmptyToast.SetHeadline("Please enter an ADB address")
    adbEmptyToast.SetFirstLine("ADB address cannot be empty.")
    wintoaster.show_toast(adbEmptyToast)

def startWSA(window): # Start subsystem if not running
    os.popen('cmd /c "WsaClient /launch wsa://system"')
    window.Hide()
    startingLayout = [[gui.Text("WSA Sideloader is attempting to start the subsystem.\nIf it's properly installed, you should see a separate window saying it's starting.\nOnce it closes, click OK to go back and try again.",font=("Calibri",11))],[RoundedButton('OK',0.3,font="Calibri 11")]]
    startingWindow = gui.Window("Message",startingLayout,icon="icon.ico",debugger_enabled=False)
    while True:
        event,values = startingWindow.Read()
        if event is None:
            sys.exit(0)
        elif event == "OK":
            startingWindow.Close()
            window.UnHide()
            break

def main():
    # Main window
    layout = [[gui.Text('Choose APK file to install:',font="Calibri 11")],
            [gui.Input(explorerfile,font="Calibri 11"),gui.FileBrowse(file_types=(("APK files","*.apk"),),font="Calibri 11")],
            [RoundedButton("View APK permissions",0.3,font="Calibri 11")],
            [gui.Text('ADB address:',font="Calibri 11")],
            [gui.Input('127.0.0.1:58526',font="Calibri 11")],
            [RoundedButton('Install',0.3,font="Calibri 11"),RoundedButton('Installed apps',0.3,font="Calibri 11"),RoundedButton('Help',0.3,font="Calibri 11"),RoundedButton('About',0.3,font="Calibri 11")]]

    window = gui.Window('WSA Sideloader', layout,icon="icon.ico",debugger_enabled=False)

    while True:
        event, values = window.Read()
        if event is None:
            sys.exit(0)
        if event == "View APK permissions":
            source_filename = values[0]
            if os.path.exists(source_filename) == False:
                permError = ToastText3()
                permError.SetHeadline("Cannot get permissions")
                permError.SetFirstLine("APK file not found.")
                wintoaster.show_toast(permError)
            else:
                source_filename = values[0]
                window.Hide()
                gui.popup_scrolled(os.popen('cmd /c "cd adbfiles & aapt d permissions "'+source_filename+'""').read(),size=(100,10),icon="icon.ico",title="APK permissions")
                window.UnHide()
        if event == "Installed apps": # Launch apps list of com.android.settings
            autostart = os.popen('cmd /c "tasklist"')
            startoutput = str(autostart.readlines())
            if "WsaClient.exe" not in startoutput:
                startWSA(window)
            else:
                try:
                    address = values[1]
                    address = address.replace(" ", "")
                    command = os.popen('cmd /c "cd adbfiles & adb connect '+address+' & adb -s '+address+' shell am start -n "com.android.settings/.applications.ManageApplications""')
                    output = command.readlines()
                    check = str(output[len(output)-1])
                    if check.startswith("Starting: Intent { cmp=com.android.settings/.applications.ManageApplications }"):
                        pass
                    else:
                        instAppsError = ToastText3()
                        instAppsError.SetHeadline("Failed to perform operation")
                        instAppsError.SetFirstLine("Please check that WSA is running and the correct ADB address has been entered.")
                        wintoaster.show_toast(instAppsError)
                except IndexError:
                    adbEmpty()
        if event == "Install":
            source_filename = values[0]
            address = values[1]
            address = address.replace(" ", "")
            if source_filename == "":
                EmptyFileName = ToastText3()
                EmptyFileName.SetHeadline("No APK file provided")
                EmptyFileName.SetFirstLine("Please select an APK file.")
                wintoaster.show_toast(EmptyFileName)
            elif exists(source_filename) == False:
                FileNotFound = ToastText3()
                FileNotFound.SetHeadline("File not found")
                FileNotFound.SetFirstLine("Please check the file path and try again.")
                wintoaster.show_toast(FileNotFound)
            elif source_filename.endswith(".apk") == False:
                UnsupportedFileType = ToastText3()
                UnsupportedFileType.SetHeadline("Unsupported file type")
                UnsupportedFileType.SetFirstLine("Only APK files are supported.")
                wintoaster.show_toast(UnsupportedFileType)
            else:
                if address == "":
                    adbEmpty()
                else:
                    autostart = os.popen('cmd /c "tasklist"')
                    startoutput = str(autostart.readlines())
                    if "WsaClient.exe" in startoutput:
                        break
                    else:
                        startWSA(window)
        if event == "Help":
            window.Hide()
            helpLayout = [[gui.Text("This program is used to install APK files on Windows Subsystem for Android. Before using WSA Sideloader, make sure you:\n1. Installed Windows Subsystem for Android\n2. Enabled developer mode (open Windows Subsystem for Android Settings which can be found in your start menu and enable developer mode)\nWSA Sideloader also integrates with File Explorer and other supported programs, allowing APKs to be installed by just (double) clicking the file.\nFor more information and support, visit the GitHub page.",font=("Calibri",11))],[RoundedButton("Back",0.3,font="Calibri 11"),RoundedButton("GitHub",0.3,font="Calibri 11")]]
            helpWindow = gui.Window('Help',helpLayout,icon="icon.ico",debugger_enabled=False)
            while True:
                event,values = helpWindow.Read()
                if event is None:
                    sys.exit(0)
                elif event == "Back":
                    helpWindow.Close()
                    window.UnHide()
                    break
                elif event == "GitHub":
                    webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader",2)
        if event == "About":
            window.Hide()
            abtLayout = [[gui.Text('WSA Sideloader is a tool which can be used to easily install apps on Windows Subsystem for Android.\nThe program has been designed with simplicity and ease of use in mind.',font="Calibri 11")],[gui.Text("Application version: "+version,font="Calibri 11")],[gui.Text("Downloaded from: "+installsource,font="Calibri 11")],[RoundedButton("Back",0.3,font="Calibri 11"),RoundedButton("GitHub",0.3,font="Calibri 11")]]
            abtWindow = gui.Window('About',abtLayout,icon="icon.ico",debugger_enabled=False)
            while True:
                event,values = abtWindow.Read()
                if event is None:
                    sys.exit(0)
                elif event == "Back":
                    abtWindow.Close()
                    window.UnHide()
                    break
                elif event == "GitHub":
                    webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader",2)

    window.Close()

    layout = [[gui.Text('Installing application, please wait...',font=("Calibri",11))]]
    window = gui.Window('Please wait...', layout,no_titlebar=True,keep_on_top=True,debugger_enabled=False)
    event, values = window.Read(timeout=0)
    command = os.popen('cmd /c "cd adbfiles & adb connect '+address+' & adb -s '+address+' install "'+source_filename+'""') # Command to install APK
    output = command.readlines()
    check = str(output[len(output)-1])
    window.Close()
    
    # Check if apk installed successfully
    if check.startswith("Success"):
        layout = [[gui.Text('The application has been successfully installed.',font=("Calibri",11))],
                [RoundedButton("Open app",0.3,font="Calibri 11"),RoundedButton("Install another APK",0.3,font="Calibri 11")]]
        window = gui.Window('Information', layout,icon="icon.ico",debugger_enabled=False)

        event, values = window.Read()
        if event == "Open app":
            getpackage = os.popen('cmd /c "cd adbfiles & aapt d permissions "'+source_filename+'""')
            pkgoutput = getpackage.readlines()
            pkgname = str(pkgoutput[0])
            webbrowser.open("wsa://"+pkgname[9:],2)
            sys.exit(0)
        elif event == "Install another APK":
            window.Close()
            main()
        else:
            sys.exit(0)
    else:
        layout = [[gui.Text('WSA Sideloader could not install the application. Please check that:\nThe APK file is valid\nWSA is running\nDev mode is enabled and the correct address has been entered',font=("Calibri",11))],
                [RoundedButton("OK",0.3,font="Calibri 11"),RoundedButton("Report a bug",0.3,font="Calibri 11")]]
        window = gui.Window('Error', layout,icon="icon.ico",debugger_enabled=False)

        event, values = window.Read()
        if event == "OK":
            window.Close()
            main()
        elif event == "Report a bug": # Open WSA Sideloader issues page
            window.Close()
            webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader/issues",2)
            sys.exit(0)
        else:
            sys.exit(0)

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    if len(sys.argv) >1:
        startgit(sys.argv[1])
    else:
        startgit()