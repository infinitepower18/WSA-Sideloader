import os
import subprocess
import PySimpleGUI as gui
import platform
import webbrowser
import sys
import ctypes
import shutil
from pkg_resources import parse_version
from button import RoundedButton
import darkdetect
from os.path import exists
import requests
from configparser import ConfigParser
import textwrap
import time
import locale
import json

# Block usage on non Windows OS
if(platform.system() != "Windows"):
    print("This operating system is not supported.")
    sys.exit(0)

ctypes.windll.shcore.SetProcessDpiAwareness(True) # Make program DPI aware
lang = locale.windows_locale[ ctypes.windll.kernel32.GetUserDefaultUILanguage() ] # Get Windows display language
strings = {}

# Load translation file if available, otherwise fallback to English US
if os.path.exists("./locales/"+lang+".json"):
    with open("./locales/"+lang+".json") as json_file:
        data = json.load(json_file)
        strings = data
else:
    with open("./locales/en-US.json") as json_file:
        data = json.load(json_file)
        strings = data

version = "1.4.0" # Version number
adbRunning = False
startCode = 0
msixfolder = os.getenv('LOCALAPPDATA') + "\\Packages\\46954GamenologyMedia.WSASideloader-APKInstaller_cjpp7y4c11e3w\\LocalState"

config = ConfigParser()
configpath = 'config.ini'

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
    main()
    
def startstore(filearg = ""): # For Microsoft Store installs
    global installsource
    installsource = "Microsoft Store"
    global explorerfile
    explorerfile = filearg
    if os.path.isdir(msixfolder+'\\platform-tools') == False: # Check if platform tools present
        shutil.copytree("platform-tools",msixfolder + "\\platform-tools")
        copyfiles = ['icon.ico','aapt.exe']
        for f in copyfiles:
            shutil.copy(f,msixfolder)
        os.chdir(msixfolder)
        main()
    else:
        os.chdir(msixfolder)
        main()

def start(filearg = ""): # For GitHub installs
    global installsource
    installsource = "GitHub"
    global explorerfile
    explorerfile = filearg
    global configpath
    configpath = os.getenv('LOCALAPPDATA') + "\\WSA Sideloader\\config.ini"
    try:
        response = requests.get("https://api.github.com/repos/infinitepower18/WSA-Sideloader/releases/latest")
        latestver = response.json()["tag_name"][1::]
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
    except requests.exceptions.RequestException as error: # Skip update check in case of network error
        main()

def startWSA(window):
    global startCode
    seconds = 30
    while seconds > 0:
        if startCode == 0:
            if(seconds != 1):
                window["_MESSAGE_"].Update("Installation will continue in "+str(seconds)+" seconds.")
            else:
                window["_MESSAGE_"].Update("Installation will continue in 1 second.")
            seconds = seconds - 1
            time.sleep(1)
        else:
            break
    window.write_event_value(('-THREAD ENDED-', '** DONE **'), 'Done!')

def installAPK(address,fname,window):
    global adbRunning
    adbRunning = True
    command = subprocess.Popen('cmd /c "cd platform-tools & adb connect '+address+' & adb -s '+address+' install "'+fname+'""', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8') # Connect to WSA and install APK
    stdout = command.stdout.readlines()
    stderr = command.stderr.readlines()
    try:
        window.write_event_value(('-OUT-', str(stdout[len(stdout)-1])),"out")
    except IndexError:
        window.write_event_value(('-OUT-', ""),"out")
    try:
        window.write_event_value(('-ERR-', str(stderr[len(stderr)-1])),"err")
    except IndexError:
        window.write_event_value(('-ERR-', ""),"err")
    window.write_event_value(('-THREAD ENDED-', '** DONE **'), 'Done!')

def main():
    global adbRunning
    global explorerfile
    global startCode
    adbAddress = "127.0.0.1:58526"
    try:
        config.read(configpath)
        adbAddress = config.get('Application','adbAddress')
    except:
        if not os.path.exists(os.getenv('LOCALAPPDATA') + "\\WSA Sideloader"):
            os.makedirs(os.getenv('LOCALAPPDATA') + "\\WSA Sideloader")
        config['Application'] = {'adbAddress':'127.0.0.1:58526'}
        with open(configpath, 'w') as configfile:
            config.write(configfile)

    # Check if WSA is installed
    if not os.path.exists(os.getenv('LOCALAPPDATA') + "\\Packages\\MicrosoftCorporationII.WindowsSubsystemForAndroid_8wekyb3d8bbwe"):
        if int(platform.win32_ver()[1].split('.')[2]) < 22000:
            layout = [[gui.Text("WSA installation not detected.\nWindows Subsystem for Android is not officially supported on Windows 10.",font=("Calibri",11))],
                    [RoundedButton("Exit",0.3,font="Calibri 11")]]
            window = gui.Window('WSA not installed', layout,icon="icon.ico",debugger_enabled=False)
            event, values = window.Read()
            if event == "Exit":
                sys.exit(0)
            elif event is None:
                sys.exit(0)
        else:
            layout = [[gui.Text("You need to install Windows Subsystem for Android before you can use this program.\nPlease download Amazon Appstore from the Microsoft Store, which will install the subsystem.\nChange your region setting to US if it's not available in your country.",font=("Calibri",11))],
                    [RoundedButton("Install WSA",0.3,font="Calibri 11")]]
            window = gui.Window('WSA not installed', layout,icon="icon.ico",debugger_enabled=False)
            event, values = window.Read()
            if event == "Install WSA":
                window.Close()
                webbrowser.open("ms-windows-store://pdp/?productid=9NJHK44TTKSX",2)
                sys.exit(0)
            elif event is None:
                sys.exit(0)
                
    # Main window
    layout = [[gui.Text(strings["chooseToInstall"],font="Calibri 11")],
            [gui.Input(explorerfile,font="Calibri 11"),gui.FileBrowse(file_types=(("APK files","*.apk"),),font="Calibri 11")],
            [RoundedButton(strings["viewPerms"],0.3,font="Calibri 11")],
            [gui.pin(gui.Text('Error message',key='_ERROR1_',visible=False,font="Calibri 11"))],
            [gui.Text(strings["address"],font="Calibri 11")],
            [gui.Input(adbAddress,font="Calibri 11")],
            [RoundedButton(strings["installButton"],0.3,font="Calibri 11"),RoundedButton(strings["installedAppsButton"],0.3,font="Calibri 11"),RoundedButton(strings["helpButton"],0.3,font="Calibri 11"),RoundedButton(strings["aboutButton"],0.3,font="Calibri 11")],
            [gui.pin(gui.Text("Error message",key='_ERROR2_',visible=False,font="Calibri 11"))]]

    window = gui.Window('WSA Sideloader', layout,icon="icon.ico",debugger_enabled=False)

    while True:
        event, values = window.Read()
        if event is None:
            if adbRunning == True:
                os.popen('cmd /c "cd platform-tools & adb kill-server"')
            sys.exit(0)
        if event == strings["viewPerms"]:
            source_filename = values[0]
            if os.path.exists(source_filename) == False:
                window['_ERROR1_'].Update("APK file not found")
                window["_ERROR1_"].Update(visible=True)
                window["_ERROR2_"].Update(visible=False)
            elif source_filename.endswith(".apk") == False:
                window['_ERROR1_'].Update("Only APK files are supported")
                window["_ERROR1_"].Update(visible=True)
                window["_ERROR2_"].Update(visible=False)
            else:
                window["_ERROR1_"].Update(visible=False)
                window["_ERROR2_"].Update(visible=False)
                source_filename = values[0]
                window.Hide()
                gui.popup_scrolled(os.popen('cmd /c "aapt d permissions "'+source_filename+'""').read(),size=(100,10),icon="icon.ico",title="APK permissions")
                window.UnHide()
        if event == strings["installedAppsButton"]: # Launch apps list of com.android.settings
            config.set('Application','adbAddress',values[1])
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            autostart = os.popen('cmd /c "tasklist"')
            startoutput = str(autostart.readlines())
            if "WsaClient.exe" not in startoutput:
                webbrowser.open("wsa://system",2)
                window['_ERROR2_'].Update("Starting WSA, please wait 30 seconds before trying again.")
                window["_ERROR2_"].Update(visible=True)
                window["_ERROR1_"].Update(visible=False)
            else:
                try:
                    address = values[1]
                    address = address.replace(" ", "")
                    adbRunning = True
                    command = os.popen('cmd /c "cd platform-tools & adb connect '+address+' & adb -s '+address+' shell am start -n "com.android.settings/.applications.ManageApplications""')
                    output = command.readlines()
                    check = str(output[len(output)-1])
                    if check.startswith("Starting: Intent { cmp=com.android.settings/.applications.ManageApplications }"):
                        window["_ERROR2_"].Update(visible=False)
                        window["_ERROR1_"].Update(visible=False)
                    elif check.startswith("failed to authenticate"):
                        window["_ERROR2_"].Update("Please allow the ADB connection and try again.")
                        window["_ERROR2_"].Update(visible=True)
                        window["_ERROR1_"].Update(visible=False)
                    else:
                        window['_ERROR2_'].Update("Please check that WSA is running, you allowed the ADB\nconnection and the correct ADB address has been entered.\nIf you denied the ADB connection, close and reopen WSA\nSideloader.")
                        window["_ERROR2_"].Update(visible=True)
                        window["_ERROR1_"].Update(visible=False)
                except IndexError:
                    window['_ERROR2_'].Update("ADB address cannot be empty")
                    window["_ERROR2_"].Update(visible=True)
                    window["_ERROR1_"].Update(visible=False)
        if event == strings["installButton"]:
            config.set('Application','adbAddress',values[1])
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            source_filename = values[0]
            address = values[1]
            address = address.replace(" ", "")
            if source_filename == "":
                window['_ERROR2_'].Update("Please select an APK file.")
                window["_ERROR2_"].Update(visible=True)
                window["_ERROR1_"].Update(visible=False)
            elif exists(source_filename) == False:
                window['_ERROR2_'].Update("APK file not found")
                window["_ERROR2_"].Update(visible=True)
                window["_ERROR1_"].Update(visible=False)
            elif source_filename.endswith(".apk") == False:
                window['_ERROR2_'].Update("Only APK files are supported")
                window["_ERROR2_"].Update(visible=True)
                window["_ERROR1_"].Update(visible=False)
            else:
                if address == "":
                    window['_ERROR2_'].Update("ADB address cannot be empty")
                    window["_ERROR2_"].Update(visible=True)
                    window["_ERROR1_"].Update(visible=False)
                else:
                    autostart = os.popen('cmd /c "tasklist"')
                    startoutput = str(autostart.readlines())
                    if "WsaClient.exe" in startoutput:
                        break
                    else:
                        webbrowser.open("wsa://system",2)
                        window.Hide()
                        startingLayout = [[gui.Text("Please wait while WSA starts.",font="Calibri 11")],
                                          [gui.Text("",key='_MESSAGE_',font="Calibri 11")],
                                          [RoundedButton("Install now",0.3,key="_INSTALL_",font="Calibri 11"),RoundedButton("Cancel",0.3,key="_CANCEL_",font="Calibri 11")]]
                        startingWindow = gui.Window('Starting WSA',startingLayout,icon="icon.ico",debugger_enabled=False,finalize=True,no_titlebar=True,keep_on_top=True)
                        startingWindow.start_thread(lambda: startWSA(startingWindow), ('-THREAD-','-THREAD ENDED-'))
                        while True:
                            event, values = startingWindow.Read()
                            if event[0] == '-THREAD ENDED-':
                                startingWindow.close()
                                break
                            if event == "_INSTALL_":
                                startingWindow["_INSTALL_"].Update(visible=False)
                                startingWindow["_CANCEL_"].Update(visible=False)
                                startCode = 1
                                startingWindow['_MESSAGE_'].Update("Installing application...")
                            if event == "_CANCEL_":
                                startingWindow["_INSTALL_"].Update(visible=False)
                                startingWindow["_CANCEL_"].Update(visible=False)
                                startCode = 2
                                startingWindow['_MESSAGE_'].Update("Cancelling...")
                        if startCode == 2:
                            startCode = 0
                            window.UnHide()
                        else:
                            startCode = 0
                            break
        if event == strings["helpButton"]:
            window["_ERROR1_"].Update(visible=False)
            window["_ERROR2_"].Update(visible=False)
            window.Hide()
            helpLayout = [[gui.Text("This program is used to install APK files on Windows Subsystem for Android. Before using WSA Sideloader, make sure you:\n1. Installed Windows Subsystem for Android\n2. Enabled developer mode (open WSA Settings and enable developer mode)\nWSA Sideloader also integrates with File Explorer and other supported programs, allowing APKs to be installed by just (double) clicking the file.\nFor more information and support, visit the GitHub page.",font=("Calibri",11))],[RoundedButton("Back",0.3,font="Calibri 11"),RoundedButton("WSA Settings",0.3,font="Calibri 11"),RoundedButton("GitHub",0.3,font="Calibri 11"),RoundedButton("Compatible apps",0.3,font="Calibri 11")]]
            helpWindow = gui.Window('Help',helpLayout,icon="icon.ico",debugger_enabled=False)
            while True:
                event,values = helpWindow.Read()
                if event is None:
                    if adbRunning == True:
                        os.popen('cmd /c "cd platform-tools & adb kill-server"')
                    sys.exit(0)
                elif event == "Back":
                    helpWindow.Close()
                    window.UnHide()
                    break
                elif event == "WSA Settings":
                    webbrowser.open("wsa-settings://",2)
                elif event == "GitHub":
                    webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader",2)
                elif event == "Compatible apps":
                    webbrowser.open("https://github.com/riverar/wsa-app-compatibility",2)
        if event == strings["aboutButton"]:
            window["_ERROR1_"].Update(visible=False)
            window["_ERROR2_"].Update(visible=False)
            window.Hide()
            abtLayout = [[gui.Text('WSA Sideloader is a tool that is used to easily install APK files on Windows Subsystem for Android.\nThe program has been designed with simplicity and ease of use in mind.',font="Calibri 11")],[gui.Text("Application version: "+version,font="Calibri 11")],[gui.Text("Downloaded from: "+installsource,font="Calibri 11")],[RoundedButton("Back",0.3,font="Calibri 11"),RoundedButton("GitHub",0.3,font="Calibri 11")]]
            abtWindow = gui.Window('About',abtLayout,icon="icon.ico",debugger_enabled=False)
            while True:
                event,values = abtWindow.Read()
                if event is None:
                    if adbRunning == True:
                        os.popen('cmd /c "cd platform-tools & adb kill-server"')
                    sys.exit(0)
                elif event == "Back":
                    abtWindow.Close()
                    window.UnHide()
                    break
                elif event == "GitHub":
                    webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader",2)

    window.Close()
    explorerfile = source_filename
    layout = [[gui.Text('Installing application, please wait...',font=("Calibri",11))]]
    window = gui.Window('Please wait...', layout,no_titlebar=True,keep_on_top=True,debugger_enabled=False)
    window.start_thread(lambda: installAPK(address, source_filename, window), ('-THREAD-','-THREAD ENDED-'))
    while True:
        event, values = window.read()
        if event[0] == '-THREAD ENDED-':
            break
        elif event[0] == '-OUT-':
            outLine = event[1]
        elif event[0] == '-ERR-':
            errLine = event[1]

    window.Close()
    
    # Check if apk installed successfully
    if outLine.startswith("Success"):
        layout = [[gui.Text('The application has been successfully installed.',font=("Calibri",11))],
                [RoundedButton("Open app",0.3,font="Calibri 11"),RoundedButton("Install another APK",0.3,font="Calibri 11")]]
        window = gui.Window('Information', layout,icon="icon.ico",debugger_enabled=False)

        event, values = window.Read()
        if event == "Open app":
            getpackage = os.popen('cmd /c "aapt d permissions "'+source_filename+'""')
            pkgoutput = getpackage.readlines()
            pkgname = str(pkgoutput[0])
            webbrowser.open("wsa://"+pkgname[9:],2)
            if adbRunning == True:
                os.popen('cmd /c "cd platform-tools & adb kill-server"')
            sys.exit(0)
        elif event == "Install another APK":
            window.Close()
            explorerfile = ""
            main()
        else:
            if adbRunning == True:
                os.popen('cmd /c "cd platform-tools & adb kill-server"')
            sys.exit(0)
    elif outLine.startswith("failed to authenticate"):
        layout = [[gui.Text('Please allow the ADB connection and run the installation again.',font=("Calibri",11))],
                [RoundedButton("OK",0.3,font="Calibri 11")]]
        window = gui.Window('Message', layout,icon="icon.ico",debugger_enabled=False)

        event, values = window.Read()
        if event == "OK":
            window.Close()
            main()
        else:
            if adbRunning == True:
                os.popen('cmd /c "cd platform-tools & adb kill-server"')
            sys.exit(0)
    else:
        if errLine == "":
            errInfo = '\n'.join(map(str,textwrap.wrap(outLine,80)))
        elif outLine == "":
            errInfo = '\n'.join(map(str,textwrap.wrap(errLine,80)))
        else:
            errInfo = '\n'.join(map(str,textwrap.wrap(outLine,80)))+'\n'+'\n'.join(map(str,textwrap.wrap(errLine,80)))
        layout = [[gui.Text('Unable to install the application. Please check that:\nThe APK file is valid\nWSA is running\nDev mode is enabled in WSA settings and the correct address has been entered\nYou allowed the ADB connection. If you denied by mistake, close and reopen WSA Sideloader.\n\n[Error Info]\n'+errInfo,font=("Calibri",11))],
                [RoundedButton("OK",0.3,font="Calibri 11"),RoundedButton("WSA Settings",0.3,font="Calibri 11"),RoundedButton("Report bug",0.3,font="Calibri 11")]]
        window = gui.Window('Error', layout,icon="icon.ico",debugger_enabled=False)

        while True:
            event, values = window.Read()
            if event == "OK":
                break
            elif event == "Report bug": # Open WSA Sideloader issues page
                webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader/issues",2)
            elif event == "WSA Settings":
                webbrowser.open("wsa-settings://",2)
            else:
                if adbRunning == True:
                    os.popen('cmd /c "cd platform-tools & adb kill-server"')
                sys.exit(0)
        window.Close()
        main()
         
"""
Which start function is called depends on how it will be deployed.
startgit if launched from git repo
start if it is being packaged into an installer
startstore for Microsoft Store distribution
Change below to appropriate function if necessary.
"""

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    if len(sys.argv) >1:
        startgit(sys.argv[1])
    else:
        startgit()
