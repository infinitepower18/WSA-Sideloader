import subprocess
import time

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