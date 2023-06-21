import hashlib
import os
import subprocess
import time
import zipfile
import PySimpleGUI as gui
from button import RoundedButton
from configparser import ConfigParser
import webbrowser
import sys
import json

def escaped_filename(filename): # Escape special characters used by cmd
    filename = list(filename)
    for i in range(len(filename)):
        if filename[i] == "&":
            filename[i] = "^&"
        elif filename[i] == "|":
            filename[i] = "^|"
        elif filename[i] == "(":
            filename[i] = "^("
        elif filename[i] == ")":
            filename[i] = "^)"
        elif filename[i] == "<":
            filename[i] = "^<"
        elif filename[i] == ">":
            filename[i] = "^>"
        elif filename[i] == "^":
            filename[i] = "^^"
    return ''.join(filename)

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

def extractBundle(fname,source):
    sha256_hash = hashlib.sha256() # Get hash to distinguish between multiple versions stored in Bundles folder
    with open(fname,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    if source == "GitHub":
        with zipfile.ZipFile(fname,"r") as zip_ref:
            if os.path.exists(os.getenv('LOCALAPPDATA') + "\\WSA Sideloader\\Bundles\\"+sha256_hash.hexdigest()) == False:
                zip_ref.extractall(os.getenv('LOCALAPPDATA') + "\\WSA Sideloader\\Bundles\\"+sha256_hash.hexdigest())
            return os.getenv('LOCALAPPDATA') + "\\WSA Sideloader\\Bundles\\"+sha256_hash.hexdigest()
    else:
        with zipfile.ZipFile(fname,"r") as zip_ref:
            if os.path.exists("Bundles\\"+sha256_hash.hexdigest()) == False:
                zip_ref.extractall("Bundles\\"+sha256_hash.hexdigest())
            return os.getcwd() + "\\Bundles\\"+sha256_hash.hexdigest()
        
def bundlePermissions(bundleLocation,format):
    if format == "apkm" or format == "apks":
        gui.popup_scrolled(os.popen('cmd /c "aapt d permissions "'+os.path.join(bundleLocation, "base.apk")+'""').read(),size=(100,10),icon="icon.ico",title="View permissions")
    if format == "xapk":
        with open(os.path.join(bundleLocation, "manifest.json"), 'r') as f:
            data = json.load(f)
            gui.popup_scrolled(data['permissions'],size=(100,10),icon="icon.ico",title="View permissions")

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
    window["_PROGRESS_"].Update("Installing base APK and supporting files...")       
    command = subprocess.Popen('cmd /c "cd platform-tools & adb connect '+address+' & adb -s '+address+' install-multiple '+files+'"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8')
    stdout = command.stdout.readlines()
    stderr = command.stderr.readlines()
    try:
        if str(stdout[len(stdout)-1]).startswith("Success"):
            if os.path.exists(bundleLocation + "\\Android\\obb"):
                window["_PROGRESS_"].Update("Copying OBB files...")
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

# TODO: Complete settings page
def settings(configpath,version,source):
    config = ConfigParser()
    config.read(configpath)

    checkUpdate = ["Enabled","Disabled"]

    layout = [[gui.Text("Check for updates on application start:",font="Calibri 11"),gui.Combo(checkUpdate, size=(max(map(len, checkUpdate))+1, 5), enable_events=True, default_value=config.get('Application','checkUpdates',fallback="Enabled"), key='-COMBO-',readonly=True)],
        [gui.Text("ADB address:",font="Calibri 11"),gui.Input(config.get('Application','adbAddress',fallback="127.0.0.1:58526"),font="Calibri 11",size=15)],
        [gui.Text("View extracted bundles:",font="Calibri 11"),RoundedButton("View",0.3,font="Calibri 11")],
        [gui.Text("Application version: "+version,font="Calibri 11")],
        [gui.Text("Downloaded from: "+source,font="Calibri 11")],
        [RoundedButton("Save",0.3,font="Calibri 11"),RoundedButton("Cancel",0.3,font="Calibri 11"),RoundedButton("Donate",0.3,font="Calibri 11")]]

    window = gui.Window('Settings', layout,icon="icon.ico",debugger_enabled=False)

    while True:
        event, values = window.read()
        if event == "Save":
            window.Close()
            # Code to save to config file
            break
        elif event == "Cancel":
            window.Close()
            break
        elif event == "Donate":
            webbrowser.open("https://ko-fi.com/F1F1K06VY",2)
        elif event == "View":
            subprocess.Popen('explorer "'+os.getcwd()+'\\Bundles"')
        else:
            sys.exit(0)