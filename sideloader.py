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
from button import RoundedButton
import subprocess

#ctypes.windll.shcore.SetProcessDpiAwareness(True) # Make program DPI aware (temp. disabled due to visual bugs)
version = "1.2.0"
gui.theme("LightGrey")
gui.theme_background_color("#232020")
gui.theme_text_element_background_color("#232020")
gui.theme_text_color("White")
gui.theme_button_color(('#232020', '#ADD8E6'))
gui.theme_input_background_color('#ADD8E6')
gui.theme_input_text_color('#000000')

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

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
        layout = [[gui.Text('You need Windows 11 to use WSA Sideloader (as well as the subsystem itself). Please upgrade your operating system and install WSA before running this program.\nFor more information and support, visit the WSA Sideloader GitHub page.')],
                [gui.Exit(),gui.Button("GitHub")]]
        window = gui.Window('Unsupported OS', layout,icon="icon.ico")

        event, values = window.Read()
        if event == "GitHub":
            window.Close()
            webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader/",2)
            sys.exit(0)
        elif event is None or "Exit":
            sys.exit(0)
        window.Close()

    # Main window
    layout = [[gui.Text('Choose APK file to install:',font="Calibri 11")],
            [gui.Input(),gui.FileBrowse(file_types=(("APK files","*.apk"),),font="Calibri 11")],
            [RoundedButton("APK permissions",0.3,font="Calibri 11")],
            [gui.Text('ADB address:',font="Calibri 11")],
            [gui.Input('127.0.0.1:58526')],
            [RoundedButton('Install',0.3,font="Calibri 11"),RoundedButton('Installed apps',0.3,font="Calibri 11"),RoundedButton('Help',0.3,font="Calibri 11"),RoundedButton('About',0.3,font="Calibri 11")]]

    window = gui.Window('WSA Sideloader', layout,icon="icon.ico")

    while True:
        event, values = window.Read()
        if event is None:
            sys.exit(0)
        if event == "APK permissions":
            source_filename = values[0]
            if os.path.exists(source_filename) == False:
                notification.notify(title="Cannot get permissions",message="APK file not found.", app_name="WSA Sideloader",app_icon="icon.ico",timeout=5)
            else:
                source_filename = values[0]
                window.Hide()
                gui.popup_scrolled(os.popen('cmd /c "aapt d permissions "'+source_filename+'""').read(),size=(100,10),icon="icon.ico",title="APK permissions")
                window.UnHide()
        if event == "Installed apps": # Launch apps list of com.android.settings
            if process_exists('WsaClient.exe') == False:
                os.popen('cmd /c "WsaClient /launch wsa://system"')
                window.Hide()
                startingLayout = [[gui.Text("WSA Sideloader is attempting to start the subsystem.\nIf it's properly installed, you should see a separate window saying it's starting.\nOnce it closes, click OK to go back and try again.",font=("Calibri",11))],[RoundedButton('OK',0.3,font="Calibri 11")]]
                startingWindow = gui.Window("Message",startingLayout,icon="icon.ico")
                while True:
                    event,values = startingWindow.Read()
                    if event is None:
                        sys.exit(0)
                    elif event == "OK":
                        startingWindow.Close()
                        window.UnHide()
                        break
            else:
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
                if process_exists('WsaClient.exe'):
                    break
                else:
                    os.popen('cmd /c "WsaClient /launch wsa://system"')
                    window.Hide()
                    startingLayout = [[gui.Text("WSA Sideloader is attempting to start the subsystem.\nIf it's properly installed, you should see a separate window saying it's starting.\nOnce it closes, click OK to go back and try again.",font=("Calibri",11))],[RoundedButton('OK',0.3,font="Calibri 11")]]
                    startingWindow = gui.Window("Message",startingLayout,icon="icon.ico")
                    while True:
                        event,values = startingWindow.Read()
                        if event is None:
                            sys.exit(0)
                        elif event == "OK":
                            startingWindow.Close()
                            window.UnHide()
                            break
        if event == "Help":
            window.Hide()
            helpLayout = [[gui.Text("This program is used to install APK files on Windows Subsystem for Android. Before using WSA Sideloader, make sure you:\n1. Installed Windows Subsystem for Android\n2. Enabled developer mode (open Windows Subsystem for Android Settings which can be found in your start menu and enable developer mode)\nIt is also recommended you select continuous mode.\nFor more information and support, visit the GitHub page.")],[gui.Button("Back"),gui.Button("GitHub")]]
            helpWindow = gui.Window('Help',helpLayout,icon="icon.ico")
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
            abtLayout = [[gui.Text('WSA Sideloader is a tool which can be used to easily install apps on Windows Subsystem for Android. The program has been designed with simplicity and ease of use in mind.',font="Calibri 11")],[gui.Text("Application version: "+version,font="Calibri 11")],[gui.Text("Python version: "+sys.version,font="Calibri 11")],[gui.Text("PySimpleGUI version: "+gui.version,font="Calibri 11")],[gui.Text("Android SDK platform tools version: "+sdkversion,font="Calibri 11")],[gui.Text("Downloaded from: "+installsource,font="Calibri 11")],[RoundedButton("Back",0.3,font="Calibri 11"),RoundedButton("GitHub",0.3,font="Calibri 11")]]
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