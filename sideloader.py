import os
import PySimpleGUI as gui
import platform
import webbrowser
import sys
import urllib
import urllib.error
from jproperties import Properties
from plyer import notification
import ctypes
from pkg_resources import parse_version

ctypes.windll.shcore.SetProcessDpiAwareness(True) # Make program DPI aware
version = "1.1.9"

def startstore(): # For Microsoft Store installs
    global installsource
    installsource = "Microsoft Store"
    try:
        file = urllib.request.urlopen("https://github.com/infinitepower18/WSA-Sideloader/raw/main/latestversion.txt")
        lines = [line.decode("utf-8") for line in file]
        latestver = lines[1].rstrip()
        if parse_version(latestver) > parse_version(version):
            layout = [[gui.Text('A newer version of WSA Sideloader is available.\nVisit the Microsoft Store to download the latest version.')],
                [gui.Button('Update now'),gui.Button('Later')]]
            window = gui.Window('Update available', layout,icon="icon.ico")
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

def startpypi(): # For PyPi installs
    global installsource
    os.chdir(__file__.strip("sideloader.py"))
    installsource = "PyPi"
    try:
        file = urllib.request.urlopen("https://github.com/infinitepower18/WSA-Sideloader/raw/main/latestversion.txt")
        lines = [line.decode("utf-8") for line in file]
        latestver = lines[2].rstrip()
        if parse_version(latestver) > parse_version(version):
            layout = [[gui.Text('A newer version of WSA Sideloader is available.\nUpdate using pip to get the latest version.')],
                [gui.Button('OK')]]
            window = gui.Window('Update available', layout,icon="icon.ico")
            event, values = window.Read()
            if event is None:
                sys.exit(0)
            elif event == "OK":
                window.Close()
                main()
        else:
            main()
    except (urllib.error.URLError,urllib.error.HTTPError,urllib.error.ContentTooShortError) as error: # Skip update check in case of network error
        main()

def start(): # For GitHub installs
    global installsource
    installsource = "GitHub"
    try:
        file = urllib.request.urlopen("https://github.com/infinitepower18/WSA-Sideloader/raw/main/latestversion.txt")
        lines = [line.decode("utf-8") for line in file]
        latestver = lines[0].rstrip()
        if parse_version(latestver) > parse_version(version):
            layout = [[gui.Text('A newer version of WSA Sideloader is available.\nWould you like to update now?')],
                [gui.Yes(),gui.No()]]
            window = gui.Window('Update available', layout,icon="icon.ico")
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
    

def main():
    # Get platform tools version for about page
    if os.path.exists('platform-tools/source.properties'):
        configs = Properties()
        with open('platform-tools/source.properties','rb') as sdkproperties:
            configs.load(sdkproperties)
            sdkversion = configs["Pkg.Revision"].data
    else:
        sdkversion = "Unknown"
            
    # Check if OS is Windows 11
    if int((platform.version().split('.')[2])) < 22000:
        layout = [[gui.Text('Sorry! WSA Sideloader will only run on Windows 11.')],
                [gui.Exit()]]
        window = gui.Window('Unsupported OS', layout,icon="icon.ico")

        event, values = window.Read()
        if event is None or "Exit":
            sys.exit(0)
        window.Close()

    # Main window
    layout = [[gui.Text('Choose APK file to install:')],
            [gui.Input(),gui.FileBrowse(file_types=(("APK files","*.apk"),))],
            [gui.Text('ADB address:')],
            [gui.Input('127.0.0.1:58526')],
            [gui.Button('Install'),gui.Button('Installed apps'),gui.Button('About WSA Sideloader')]]

    window = gui.Window('WSA Sideloader', layout,icon="icon.ico")

    while True:
        event, values = window.Read()
        if event is None:
            sys.exit(0)
        if event == "Installed apps": # Launch apps list of com.android.settings
            try:
                address = values[1]
                address = address.replace(" ", "")
                command = os.popen('cmd /c "cd platform-tools & adb connect '+address+' & adb -s '+address+' shell am start -n "com.android.settings/.applications.ManageApplications""')
                output = command.readlines()
                check = str(output[len(output)-1])
                if check.startswith("Starting: Intent { cmp=com.android.settings/.applications.ManageApplications }"):
                    pass
                else:
                    notification.notify(title="Failed to perform operation",message="Please check that WSA is running and the correct ADB address has been entered.", app_name="WSA Sideloader",app_icon="icon.ico",timeout=5)
            except IndexError:
                notification.notify(title="Please enter an ADB address",message="ADB address cannot be empty.", app_name="WSA Sideloader",app_icon="icon.ico",timeout=5)
        if event == "Install":
            source_filename = values[0]
            address = values[1]
            address = address.replace(" ", "")
            if address == "":
                notification.notify(title="Please enter an ADB address",message="ADB address cannot be empty.", app_name="WSA Sideloader",app_icon="icon.ico",timeout=5)
            else:
                break
        if event == "About WSA Sideloader":
            window.Hide()
            abtLayout = [[gui.Text('WSA Sideloader is a tool which can be used to easily install apps on Windows Subsystem for Android. The program has been designed with simplicity and ease of use in mind.')],[gui.Text("Application version: "+version)],[gui.Text("Python version: "+sys.version)],[gui.Text("PySimpleGUI version: "+gui.version)],[gui.Text("Android SDK platform tools version: "+sdkversion)],[gui.Text("Downloaded from: "+installsource)],[gui.Button("Back"),gui.Button("GitHub")]]
            abtWindow = gui.Window('About',abtLayout,icon="icon.ico")
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

    layout = [[gui.Text('Installing application, please wait...')]]
    window = gui.Window('Please wait...', layout,no_titlebar=True,keep_on_top=True)
    event, values = window.Read(timeout=0)
    command = os.popen('cmd /c "cd platform-tools & adb connect '+address+' & adb -s '+address+' install "'+source_filename+'""') # Command to install APK
    output = command.readlines()
    check = str(output[len(output)-1])
    window.Close()
    
    # Check if apk installed successfully
    if check.startswith("Success"):
        layout = [[gui.Text('The application has been successfully installed.')],
                [gui.Exit(),gui.Button('Install another APK')]]
        window = gui.Window('Information', layout,icon="icon.ico")

        event, values = window.Read()
        if event == "Install another APK":
            window.Close()
            main()
        else:
            sys.exit(0)
    else:
        layout = [[gui.Text('WSA Sideloader could not install the application. Please check that:\nThe APK file is valid\nWSA is running\nDev mode is enabled and the correct address has been entered')],
                [gui.Button('OK'),gui.Button('Report a bug')]]
        window = gui.Window('Error', layout,icon="icon.ico")

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
    start()