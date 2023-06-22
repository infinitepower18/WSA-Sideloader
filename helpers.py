import hashlib
import os
import subprocess
import zipfile

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

def extractBundle(fname,source,window):
    sha256_hash = hashlib.sha256() # Get hash to distinguish between multiple versions stored in Bundles folder
    location = ""
    with open(fname,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    if source == "GitHub":
        with zipfile.ZipFile(fname,"r") as zip_ref:
            if os.path.exists(os.getenv('LOCALAPPDATA') + "\\WSA Sideloader\\Bundles\\"+sha256_hash.hexdigest()) == False:
                zip_ref.extractall(os.getenv('LOCALAPPDATA') + "\\WSA Sideloader\\Bundles\\"+sha256_hash.hexdigest())
            location = os.getenv('LOCALAPPDATA') + "\\WSA Sideloader\\Bundles\\"+sha256_hash.hexdigest()
    elif source == "Microsoft Store":
        with zipfile.ZipFile(fname,"r") as zip_ref:
            if os.path.exists(os.getenv('LOCALAPPDATA') + "\\Packages\\46954GamenologyMedia.WSASideloader-APKInstaller_cjpp7y4c11e3w\\TempState\\Bundles\\"+sha256_hash.hexdigest()) == False:
                zip_ref.extractall(os.getenv('LOCALAPPDATA') + "\\Packages\\46954GamenologyMedia.WSASideloader-APKInstaller_cjpp7y4c11e3w\\TempState\\Bundles\\"+sha256_hash.hexdigest())
            location = os.getenv('LOCALAPPDATA') + "\\Packages\\46954GamenologyMedia.WSASideloader-APKInstaller_cjpp7y4c11e3w\\TempState\\Bundles\\"+sha256_hash.hexdigest()   
    else:
        with zipfile.ZipFile(fname,"r") as zip_ref:
            if os.path.exists("Bundles\\"+sha256_hash.hexdigest()) == False:
                zip_ref.extractall("Bundles\\"+sha256_hash.hexdigest())
            location = os.getcwd() + "\\Bundles\\"+sha256_hash.hexdigest()
    window.write_event_value(('-OUT-', location),"out")
    window.write_event_value(('-THREAD ENDED-', '** DONE **'), 'Done!')