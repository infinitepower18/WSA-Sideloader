import os
import PySimpleGUI as gui
import platform
import webbrowser
import sys
import ctypes
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
from helpers import *

# Block usage on non Windows OS
if(platform.system() != "Windows"):
    print("This operating system is not supported.")
    sys.exit(0)

ctypes.windll.shcore.SetProcessDpiAwareness(True) # Make program DPI aware
lang = locale.windows_locale[ ctypes.windll.kernel32.GetUserDefaultUILanguage() ] # Get Windows display language
strings = {}

# Load translation file if available, otherwise fallback to English US
if os.path.exists(os.getcwd()+"\\locales\\"+lang+".json"):
    with open(os.getcwd()+"\\locales\\"+lang+".json",encoding='utf-8') as json_file:
        strings = json.load(json_file)
else:
    with open(os.getcwd()+"\\locales\\en_US.json",encoding='utf-8') as json_file:
        strings = json.load(json_file)
        
version = "1.4.0" # Version number
adbVersion = "34.0.3"
adbRunning = False
startCode = 0
icon = os.getcwd()+"\\icon.ico"
msixfolder = os.getenv('LOCALAPPDATA') + "\\Packages\\46954GamenologyMedia.WSASideloader-APKInstaller_cjpp7y4c11e3w\\TempState"
adbAddress = "127.0.0.1:58526"
checkUpdates = True

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
    installsource = strings["githubClone"]
    global explorerfile
    explorerfile = filearg
    getConfig()
    main()
    
def startstore(filearg = ""): # For Microsoft Store installs
    global installsource
    installsource = "Microsoft Store"
    global explorerfile
    explorerfile = filearg
    global configpath
    configpath = os.getenv('LOCALAPPDATA') + "\\Packages\\46954GamenologyMedia.WSASideloader-APKInstaller_cjpp7y4c11e3w\\LocalState\\config.ini"
    getConfig()
    main()

def start(filearg = ""): # For GitHub installs
    global installsource
    installsource = "GitHub"
    global explorerfile
    explorerfile = filearg
    global configpath
    configpath = os.getenv('LOCALAPPDATA') + "\\WSA Sideloader\\config.ini"
    getConfig()
    if checkUpdates:
        try:
            response = requests.get("https://api.github.com/repos/infinitepower18/WSA-Sideloader/releases/latest")
            latestver = response.json()["tag_name"][1::]
            if parse_version(latestver) > parse_version(version):
                layout = [[gui.Text(strings["newUpdate"],font=("Calibri",11))],
                    [RoundedButton(strings["yesButton"],0.3,font="Calibri 11"),RoundedButton(strings["noButton"],0.3,font="Calibri 11")]]
                window = gui.Window(strings["updateAvailable"], layout,icon=icon,debugger_enabled=False)
                event, values = window.Read()
                if event is None:
                    sys.exit(0)
                elif event == strings["yesButton"]:
                    window.Close()
                    webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader/releases/latest",2)
                    sys.exit(0)
                elif event == strings["noButton"]:
                    window.Close()
                    main()
            else:
                main()
        except requests.exceptions.RequestException as error: # Skip update check in case of network error
            main()
    else:
        main()

def startWSA(window):
    global startCode
    seconds = 30
    while seconds > 0:
        if startCode == 0:
            if(seconds != 1):
                window["_MESSAGE_"].Update(strings["instContinueinSeconds"].format(secs=seconds))
            else:
                window["_MESSAGE_"].Update(strings["instContinueinOneSec"])
            seconds = seconds - 1
            time.sleep(1)
        else:
            break
    window.write_event_value(('-THREAD ENDED-', '** DONE **'), 'Done!')

def getConfig():
    global adbAddress
    global checkUpdates
    if installsource == "GitHub":
        if not os.path.exists(os.getenv('LOCALAPPDATA') + "\\WSA Sideloader"):
            os.makedirs(os.getenv('LOCALAPPDATA') + "\\WSA Sideloader")
    if not os.path.exists(configpath):
        config['Application'] = {'adbAddress':'127.0.0.1:58526','checkUpdates':"Enabled"}
        with open(configpath, 'w') as configfile:
            config.write(configfile)
    config.read(configpath)
    adbAddress = config.get('Application','adbAddress',fallback="127.0.0.1:58526")
    if config.get('Application','checkUpdates',fallback="Enabled") == "Enabled":
        checkUpdates = True
    else:
        checkUpdates = False

def bundlePermissions(bundleLocation,format):
    if format == "apkm" or format == "apks":
        gui.popup_scrolled(os.popen('cmd /c "aapt d permissions "'+os.path.join(bundleLocation, "base.apk")+'""').read(),size=(100,10),icon=icon,title=strings["viewPerms"])
    if format == "xapk":
        with open(os.path.join(bundleLocation, "manifest.json"), 'r',encoding="utf-8") as f:
            data = json.load(f)
            gui.popup_scrolled(data['permissions'],size=(100,10),icon=icon,title=strings["viewPerms"])

def installBundle(bundleLocation, address, window):
    global adbRunning
    adbRunning = True
    files = ''
    for file in os.listdir(bundleLocation):
        if file.endswith(".apk"):
            if files == '':
                files = files + '"'+os.path.join(bundleLocation, file)+'"'
            else:
                files = files + " " + '"'+os.path.join(bundleLocation, file)+'"'
    window["_PROGRESS_"].Update(strings["installingBundleApks"])       
    command = subprocess.Popen('cmd /c "cd platform-tools & adb connect '+address+' & adb -s '+address+' install-multiple '+files+'"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8')
    stdout = command.stdout.readlines()
    stderr = command.stderr.readlines()
    try:
        if str(stdout[len(stdout)-1]).startswith("Success"):
            if os.path.exists(bundleLocation + "\\Android\\obb"):
                window["_PROGRESS_"].Update(strings["copyingObb"])
                for dir in os.listdir(bundleLocation + "\\Android\\obb"):
                    pushobb = subprocess.Popen('cmd /c "cd platform-tools & adb -s '+address+' shell mkdir /sdcard/Android/obb/'+dir+' & adb -s '+address+' push '+bundleLocation+'\\android\\obb\\'+dir+'\. /sdcard/Android/obb/'+dir+'/"', shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf-8')
                    while True:
                        line = pushobb.stdout.read(1)
                        if line == '' and pushobb.poll() != None:
                            break
                        if line != '':
                            sys.stdout.flush()
    except IndexError:
        pass
    try:
        window.write_event_value(('-OUT-', str(stdout[len(stdout)-1])),"out")
    except IndexError:
        window.write_event_value(('-OUT-', ""),"out")
    try:
        window.write_event_value(('-ERR-', str(stderr[len(stderr)-1])),"err")
    except IndexError:
        window.write_event_value(('-ERR-', ""),"err")
    window.write_event_value(('-THREAD ENDED-', '** DONE **'), 'Done!')

def settings(configpath,version,source):
    config = ConfigParser()
    config.read(configpath)

    checkUpdate = ["Enabled","Disabled"]

    if source == "Microsoft Store":
        layout = [[gui.Text(strings["address"],font="Calibri 11"),gui.Input(config.get('Application','adbAddress',fallback="127.0.0.1:58526"),font="Calibri 11",size=15,key='-ADDRESS-')],
            [gui.Text(strings["viewExtractedBundles"],font="Calibri 11"),RoundedButton("View",0.3,font="Calibri 11")],
            [gui.Text(strings["noBundlesFound"],key='_NOBUNDLES_',visible=False,font="Calibri 11")],
            [gui.Text(strings["abtAppVer"]+version,font="Calibri 11")],
            [gui.Text(strings["abtSource"]+source,font="Calibri 11")],
            [RoundedButton(strings["saveButton"],0.3,font="Calibri 11"),RoundedButton(strings["cancelButton"],0.3,font="Calibri 11"),RoundedButton(strings["donateButton"],0.3,font="Calibri 11")]]
    else:
        layout = [[gui.Text(strings["checkUpdatesAppStart"],font="Calibri 11"),gui.Combo(checkUpdate, size=(max(map(len, checkUpdate))+1, 5), enable_events=True, default_value=config.get('Application','checkUpdates',fallback="Enabled"), key='-CHECKUPDATES-',readonly=True)],
            [gui.Text(strings["address"],font="Calibri 11"),gui.Input(config.get('Application','adbAddress',fallback="127.0.0.1:58526"),font="Calibri 11",size=15,key='-ADDRESS-')],
            [gui.Text(strings["viewExtractedBundles"],font="Calibri 11"),RoundedButton("View",0.3,font="Calibri 11")],
            [gui.Text(strings["noBundlesFound"],key='_NOBUNDLES_',visible=False,font="Calibri 11")],
            [gui.Text(strings["abtAppVer"]+version,font="Calibri 11")],
            [gui.Text(strings["abtSource"]+source,font="Calibri 11")],
            [RoundedButton(strings["saveButton"],0.3,font="Calibri 11"),RoundedButton(strings["cancelButton"],0.3,font="Calibri 11"),RoundedButton(strings["donateButton"],0.3,font="Calibri 11")]]

    window = gui.Window(strings["settingsButton"], layout,icon=icon,debugger_enabled=False)

    while True:
        event, values = window.read()
        if event == strings["saveButton"]:
            window.Close()
            if source == "Microsoft Store":
                config['Application'] = {'adbAddress':values["-ADDRESS-"],'checkUpdates':"Enabled"}
            else:
                config['Application'] = {'adbAddress':values["-ADDRESS-"],'checkUpdates':values["-CHECKUPDATES-"]}
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            break
        elif event == strings["cancelButton"]:
            window.Close()
            break
        elif event == strings["donateButton"]:
            webbrowser.open("https://ko-fi.com/F1F1K06VY",2)
        elif event == strings["viewButton"]:
            if installsource == "Microsoft Store":
                if os.path.exists(msixfolder+'\\Bundles'):
                    subprocess.Popen('explorer "'+msixfolder+'\\Bundles"')
                else:
                    window["_NOBUNDLES_"].Update(visible=True)
            elif installsource == "GitHub":
                if os.path.exists(os.getenv('LOCALAPPDATA') + "\\WSA Sideloader\\Bundles"):
                    subprocess.Popen('explorer "'+os.getenv('LOCALAPPDATA') + '\\WSA Sideloader\\Bundles"')
                else:
                    window["_NOBUNDLES_"].Update(visible=True)
            else:
                if os.path.exists(os.getcwd()+'\\Bundles'):
                    subprocess.Popen('explorer "'+os.getcwd()+'\\Bundles"')
                else:
                    window["_NOBUNDLES_"].Update(visible=True)
        elif event is None:
            if adbRunning == True:
                os.popen('cmd /c "cd platform-tools & adb kill-server"')
            sys.exit(0)

def main():
    global adbRunning
    global explorerfile
    global startCode
    global adbAddress

    # Check if WSA is installed
    if not os.path.exists(os.getenv('LOCALAPPDATA') + "\\Packages\\MicrosoftCorporationII.WindowsSubsystemForAndroid_8wekyb3d8bbwe"):
        if int(platform.win32_ver()[1].split('.')[2]) < 22000:
            layout = [[gui.Text(strings["wsaNotDetectedWin10"],font=("Calibri",11))],
                    [RoundedButton(strings["exitButton"],0.3,font="Calibri 11")]]
            window = gui.Window(strings["wsaNotInstalled"], layout,icon=icon,debugger_enabled=False)
            event, values = window.Read()
            if event == strings["exitButton"]:
                sys.exit(0)
            elif event is None:
                sys.exit(0)
        else:
            layout = [[gui.Text(strings["wsaNotDetectedWin11"],font=("Calibri",11))],
                    [RoundedButton(strings["installWsaButton"],0.3,font="Calibri 11")]]
            window = gui.Window(strings["wsaNotInstalled"], layout,icon=icon,debugger_enabled=False)
            event, values = window.Read()
            if event == strings["installWsaButton"]:
                window.Close()
                webbrowser.open("ms-windows-store://pdp/?productid=9NJHK44TTKSX",2)
                sys.exit(0)
            elif event is None:
                sys.exit(0)
                
    # Main window
    layout = [[gui.Text(strings["chooseToInstall"],font="Calibri 11")],
            [gui.Input(explorerfile,font="Calibri 11"),gui.FileBrowse(file_types=((strings["androidFiles"],"*.apk"),(strings["androidFiles"],"*.xapk"),(strings["androidFiles"],"*.apkm"),(strings["androidFiles"],"*.apks")),font="Calibri 11")],
            [RoundedButton(strings["installButton"],0.3,font="Calibri 11"),RoundedButton(strings["viewPerms"],0.3,font="Calibri 11")],
            [gui.pin(gui.Text('Error message',key='_ERROR1_',visible=False,font="Calibri 11"))],
            [RoundedButton(strings["installedAppsButton"],0.3,font="Calibri 11"),RoundedButton(strings["settingsButton"],0.3,font="Calibri 11"),RoundedButton(strings["helpButton"],0.3,font="Calibri 11")],
            [gui.pin(gui.Text("Error message",key='_ERROR2_',visible=False,font="Calibri 11"))]]

    window = gui.Window('WSA Sideloader', layout,icon=icon,debugger_enabled=False)

    while True:
        event, values = window.Read()
        if event is None:
            if adbRunning == True:
                os.popen('cmd /c "cd platform-tools & adb kill-server"')
            sys.exit(0)
        if event == strings["viewPerms"]:
            source_filename = values[0]
            if os.path.exists(source_filename) == False:
                window['_ERROR1_'].Update(strings["apkNotFound"])
                window["_ERROR1_"].Update(visible=True)
                window["_ERROR2_"].Update(visible=False)
            elif source_filename.endswith(".apk") == False and source_filename.endswith(".apks") == False and source_filename.endswith(".apkm") == False and source_filename.endswith(".xapk") == False:
                window['_ERROR1_'].Update(strings["onlyApkSupported"])
                window["_ERROR1_"].Update(visible=True)
                window["_ERROR2_"].Update(visible=False)
            else:
                window["_ERROR1_"].Update(visible=False)
                window["_ERROR2_"].Update(visible=False)
                source_filename = values[0]
                window.Hide()
                if source_filename.endswith(".apk"):
                    try:
                        gui.popup_scrolled(os.popen('cmd /c "aapt d permissions "'+escaped_filename(source_filename)+'""').read(),size=(100,10),icon=icon,title=strings["viewPerms"])
                    except Exception as e:
                        errLayout = [[gui.Text(strings["getPermsError"]+str(e),font=("Calibri",11))],
                                     [RoundedButton(strings["reportBugButton"],0.3,font="Calibri 11"),RoundedButton(strings["backButton"],0.3,font="Calibri 11")]]
                        errWindow = gui.Window(strings["errorTitle"], errLayout,debugger_enabled=False,icon=icon)
                        while True:
                            event, values = errWindow.read()
                            if event == strings["backButton"]:
                                errWindow.Close()
                                break
                            elif event == strings["reportBugButton"]: # Open WSA Sideloader issues page
                                webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader/issues",2)
                            else:
                                if adbRunning == True:
                                    os.popen('cmd /c "cd platform-tools & adb kill-server"')
                                sys.exit(0)
                else:
                    waitLayout = [[gui.Text(strings["retrievingPerms"],font=("Calibri",11))]]
                    waitWindow = gui.Window('Please wait...', waitLayout,no_titlebar=True,keep_on_top=True,debugger_enabled=False,finalize=True)
                    waitWindow.start_thread(lambda: extractBundle(source_filename,installsource,waitWindow), ('-THREAD-','-THREAD ENDED-'))
                    while True:
                        event, values = waitWindow.read()
                        if event[0] == '-THREAD ENDED-':
                            break
                        elif event[0] == '-OUT-':
                            extractedBundle = event[1]
                    waitWindow.close()
                    try:
                        if source_filename.endswith(".apks"):
                            bundlePermissions(escaped_filename(extractedBundle),"apks")
                        elif source_filename.endswith(".apkm"):
                            bundlePermissions(escaped_filename(extractedBundle),"apkm")
                        elif source_filename.endswith(".xapk"):
                            bundlePermissions(escaped_filename(extractedBundle),"xapk")
                    except Exception as e:
                        errLayout = [[gui.Text(strings["getPermsError"]+str(e),font=("Calibri",11))],
                                     [RoundedButton(strings["reportBugButton"],0.3,font="Calibri 11"),RoundedButton(strings["backButton"],0.3,font="Calibri 11")]]
                        errWindow = gui.Window(strings["errorTitle"], errLayout,debugger_enabled=False,icon=icon)
                        while True:
                            event, values = errWindow.read()
                            if event == strings["backButton"]:
                                errWindow.Close()
                                break
                            elif event == strings["reportBugButton"]: # Open WSA Sideloader issues page
                                webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader/issues",2)
                            else:
                                if adbRunning == True:
                                    os.popen('cmd /c "cd platform-tools & adb kill-server"')
                                sys.exit(0)
                window.UnHide()
        if event == strings["installedAppsButton"]: # Launch apps list of com.android.settings
            autostart = os.popen('cmd /c "tasklist"')
            startoutput = str(autostart.readlines())
            if "WsaClient.exe" not in startoutput:
                webbrowser.open("wsa://system",2)
                window['_ERROR2_'].Update(strings["startingWait"])
                window["_ERROR2_"].Update(visible=True)
                window["_ERROR1_"].Update(visible=False)
            else:
                try:
                    address = adbAddress
                    address = address.replace(" ", "")
                    adbRunning = True
                    command = os.popen('cmd /c "cd platform-tools & adb connect '+address+' & adb -s '+address+' shell am start -n "com.android.settings/.applications.ManageApplications""')
                    output = command.readlines()
                    check = str(output[len(output)-1])
                    if check.startswith("Starting: Intent { cmp=com.android.settings/.applications.ManageApplications }"):
                        window["_ERROR2_"].Update(visible=False)
                        window["_ERROR1_"].Update(visible=False)
                    elif check.startswith("failed to authenticate"):
                        window["_ERROR2_"].Update(strings["instAppsAdbAllow"])
                        window["_ERROR2_"].Update(visible=True)
                        window["_ERROR1_"].Update(visible=False)
                    else:
                        window['_ERROR2_'].Update(strings["instAppsError"])
                        window["_ERROR2_"].Update(visible=True)
                        window["_ERROR1_"].Update(visible=False)
                except IndexError:
                    window['_ERROR2_'].Update(strings["adbEmpty"])
                    window["_ERROR2_"].Update(visible=True)
                    window["_ERROR1_"].Update(visible=False)
        if event == strings["installButton"]:
            source_filename = values[0]
            address = adbAddress
            address = address.replace(" ", "")
            if source_filename == "":
                window['_ERROR2_'].Update(strings["blankApkField"])
                window["_ERROR2_"].Update(visible=True)
                window["_ERROR1_"].Update(visible=False)
            elif exists(source_filename) == False:
                window['_ERROR2_'].Update(strings["apkNotFound"])
                window["_ERROR2_"].Update(visible=True)
                window["_ERROR1_"].Update(visible=False)
            elif source_filename.endswith(".apk") == False and source_filename.endswith(".xapk") == False and source_filename.endswith(".apkm") == False and source_filename.endswith(".apks") == False:
                window['_ERROR2_'].Update(strings["onlyApkSupported"])
                window["_ERROR2_"].Update(visible=True)
                window["_ERROR1_"].Update(visible=False)
            else:
                if address == "":
                    window['_ERROR2_'].Update(strings["adbEmpty"])
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
                        startingLayout = [[gui.Text(strings["waitWhileWsaStarts"],font="Calibri 11")],
                                          [gui.Text("",key='_MESSAGE_',font="Calibri 11")],
                                          [RoundedButton(strings["installNowButton"],0.3,key="_INSTALL_",font="Calibri 11"),RoundedButton(strings["cancelButton"],0.3,key="_CANCEL_",font="Calibri 11")]]
                        startingWindow = gui.Window('Starting WSA',startingLayout,icon=icon,debugger_enabled=False,finalize=True,no_titlebar=True,keep_on_top=True)
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
                                startingWindow['_MESSAGE_'].Update(strings["installingApp"])
                            if event == "_CANCEL_":
                                startingWindow["_INSTALL_"].Update(visible=False)
                                startingWindow["_CANCEL_"].Update(visible=False)
                                startCode = 2
                                startingWindow['_MESSAGE_'].Update(strings["cancelling"])
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
            helpLayout = [[gui.Text(strings["helpText"],font=("Calibri",11))],[RoundedButton(strings["backButton"],0.3,font="Calibri 11"),RoundedButton(strings["wsaSettingsButton"],0.3,font="Calibri 11"),RoundedButton(strings["ghButton"],0.3,font="Calibri 11"),RoundedButton(strings["compatAppsButton"],0.3,font="Calibri 11")]]
            helpWindow = gui.Window(strings["helpButton"],helpLayout,icon=icon,debugger_enabled=False)
            while True:
                event,values = helpWindow.Read()
                if event is None:
                    if adbRunning == True:
                        os.popen('cmd /c "cd platform-tools & adb kill-server"')
                    sys.exit(0)
                elif event == strings["backButton"]:
                    helpWindow.Close()
                    window.UnHide()
                    break
                elif event == strings["wsaSettingsButton"]:
                    webbrowser.open("wsa-settings://",2)
                elif event == strings["ghButton"]:
                    webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader",2)
                elif event == strings["compatAppsButton"]:
                    webbrowser.open("https://github.com/riverar/wsa-app-compatibility",2)
        if event == strings["settingsButton"]:
            window["_ERROR1_"].Update(visible=False)
            window["_ERROR2_"].Update(visible=False)
            window.Hide()
            settings(configpath=configpath,version=version,source=installsource)
            getConfig()
            window.UnHide()

    window.Close()
    explorerfile = source_filename
    if source_filename.endswith(".apk"):
        adbRunning = True
        layout = [[gui.Text(strings["installingPlsWait"],font=("Calibri",11))]]
        window = gui.Window('Please wait...', layout,no_titlebar=True,keep_on_top=True,debugger_enabled=False)
        window.start_thread(lambda: installAPK(address, escaped_filename(source_filename), window), ('-THREAD-','-THREAD ENDED-'))
    else:
        layout = [[gui.Text(strings["bundleInstallPatient"],font=("Calibri",11))],
                  [gui.Text(strings["processingFile"],key='_PROGRESS_',font="Calibri 11")]]
        window = gui.Window('Please wait...', layout,no_titlebar=True,keep_on_top=True,debugger_enabled=False,finalize=True)
        window.start_thread(lambda: extractBundle(source_filename,installsource,window), ('-THREAD-','-THREAD ENDED-'))
        while True:
            event, values = window.read()
            if event[0] == '-THREAD ENDED-':
                break
            elif event[0] == '-OUT-':
                extractedBundle = event[1]
        window.start_thread(lambda: installBundle(escaped_filename(extractedBundle),address,window), ('-THREAD-','-THREAD ENDED-'))
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
        if source_filename.endswith(".apk"):
            layout = [[gui.Text(strings["appInstalled"],font=("Calibri",11))],
                    [RoundedButton(strings["openAppButton"],0.3,font="Calibri 11"),RoundedButton(strings["installAnotherAppButton"],0.3,font="Calibri 11")]]
        else:
            layout = [[gui.Text(strings["appInstalledBundle"],font=("Calibri",11))],
                    [RoundedButton(strings["installAnotherAppButton"],0.3,font="Calibri 11")]]
        window = gui.Window(strings["infoTitle"], layout,icon=icon,debugger_enabled=False)

        event, values = window.Read()
        if event == strings["openAppButton"]: # TODO: Get this working for bundles
            getpackage = os.popen('cmd /c "aapt d permissions "'+escaped_filename(source_filename)+'""')
            pkgoutput = getpackage.readlines()
            pkgname = str(pkgoutput[0])
            webbrowser.open("wsa://"+pkgname[9:],2)
            if adbRunning == True:
                os.popen('cmd /c "cd platform-tools & adb kill-server"')
            sys.exit(0)
        elif event == strings["installAnotherAppButton"]:
            window.Close()
            explorerfile = ""
            main()
        else:
            if adbRunning == True:
                os.popen('cmd /c "cd platform-tools & adb kill-server"')
            sys.exit(0)
    elif outLine.startswith("failed to authenticate"):
        layout = [[gui.Text(strings["allowAdb"],font=("Calibri",11))],
                [RoundedButton(strings["okButton"],0.3,font="Calibri 11")]]
        window = gui.Window(strings["message"], layout,icon=icon,debugger_enabled=False)

        event, values = window.Read()
        if event == strings["okButton"]:
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
        layout = [[gui.Text(strings["unableToInstall"]+'\n'+errInfo,font=("Calibri",11))],
                [RoundedButton(strings["okButton"],0.3,font="Calibri 11"),RoundedButton(strings["wsaSettingsButton"],0.3,font="Calibri 11"),RoundedButton(strings["reportBugButton"],0.3,font="Calibri 11")]]
        window = gui.Window(strings["errorTitle"], layout,icon=icon,debugger_enabled=False)

        while True:
            event, values = window.Read()
            if event == strings["okButton"]:
                break
            elif event == strings["reportBugButton"]: # Open WSA Sideloader issues page
                webbrowser.open("https://github.com/infinitepower18/WSA-Sideloader/issues",2)
            elif event == strings["wsaSettingsButton"]:
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
