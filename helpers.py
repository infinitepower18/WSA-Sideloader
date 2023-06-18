import hashlib
import os
import subprocess
import time
import zipfile
import PySimpleGUI as gui
from button import RoundedButton

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

def extractBundle(fname,source):
    sha256_hash = hashlib.sha256() # Get hash to distinguish between multiple versions stored in Bundles folder
    with open(fname,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    if source == "GitHub":
        with zipfile.ZipFile(fname,"r") as zip_ref:
            zip_ref.extractall(os.getenv('LOCALAPPDATA') + "\\WSA Sideloader\\Bundles\\"+sha256_hash.hexdigest())
            return os.getenv('LOCALAPPDATA') + "\\WSA Sideloader\\Bundles\\"+sha256_hash.hexdigest()
    else:
        with zipfile.ZipFile(fname,"r") as zip_ref:
            zip_ref.extractall("Bundles\\"+sha256_hash.hexdigest())
            return os.getcwd() + "\\Bundles\\"+sha256_hash.hexdigest()

# TODO: Handle OBB files
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
    command = subprocess.Popen('cmd /c "cd platform-tools & adb connect '+address+' & adb -s '+address+' install-multiple '+files+'"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8')
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

# TODO: Complete settings page
def settings():
    
    apSelection = ["System","Light","Dark"]
    lgSelection = ["English US"]
    checkUpdate = ["Enabled","Disabled"]
    adbAddress = "127.0.0.1:58526"

    layout = [[gui.Text("Language:",font="Calibri 11"),gui.Combo(lgSelection, size=15, enable_events=True, key='-COMBO-')],
        [gui.Text("Appearance:",font="Calibri 11"),gui.Combo(apSelection, size=15, enable_events=True, key='-COMBO-')],
        [gui.Text("Check for updates on application start:",font="Calibri 11"),gui.Combo(checkUpdate, size=(max(map(len, apSelection))+1, 5), enable_events=True, key='-COMBO-')],
        [gui.Text("ADB address:",font="Calibri 11"),gui.Input(adbAddress,font="Calibri 11",size=15)],
        [gui.Text("View extracted bundles:",font="Calibri 11"),RoundedButton("View",0.3,font="Calibri 11")],
        [gui.Text("Application version: 1.4.0 (Latest version)",font="Calibri 11")],
        [gui.Text("Downloaded from: GitHub",font="Calibri 11")],
        [RoundedButton("Save",0.3,font="Calibri 11"),RoundedButton("Cancel",0.3,font="Calibri 11"),RoundedButton("Donate",0.3,font="Calibri 11")]]

    window = gui.Window('Settings', layout,icon="icon.ico",debugger_enabled=False)

    while True:
        event, values = window.read()
        window.Close()
        break