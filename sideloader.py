import dload
import os
import PySimpleGUI27 as gui
import platform
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

version = "1.0.1"

def main():
    if is_admin() == False: # Get admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    # Check if OS is Windows 11
    if int((platform.version().split('.')[2])) < 22000:
        layout = [[gui.Text('Sorry! WSA Sideloader will only run on Windows 11.')],
                [gui.Exit()]]
        window = gui.Window('Error', layout)

        event, values = window.Read()
        if event is None or "Exit":
            quit()
        window.Close()

    if os.path.isdir('platform-tools') == False: # Check if platform tools present
        layout = [[gui.Text('In order to function correctly, WSA Sideloader will need to download the SDK platform tools. Once downloaded, the application will launch automatically.')],
                [gui.Button('Continue')]]
        window = gui.Window('Information', layout)
        event, values = window.Read()
        if event is None:
            quit()
        window.Close()
        dload.save_unzip("https://dl.google.com/android/repository/platform-tools-latest-windows.zip",extract_path=os.getcwd(),delete_after=True)

    layout = [[gui.Text('Choose APK file to install:')],
            [gui.Input(),gui.FileBrowse()],
            [gui.Text('ADB address:')],
            [gui.Input('127.0.0.1:58526')],
            [gui.Button('Install')]]

    window = gui.Window('WSA Sideloader '+version, layout)

    event, values = window.Read()
    if event is None:
        quit()

    source_filename = values[0]
    address = values[1]

    window.Close()

    command = os.popen('cmd /c "cd platform-tools & adb connect '+address+' & adb install '+source_filename+'"')
    output = command.readlines()
    check = str(output[len(output)-1])
    if check.startswith("Success"):
        layout = [[gui.Text('The application has been successfully installed.')],
                [gui.Exit()]]
        window = gui.Window('Information', layout)

        event, values = window.Read()
        window.Close()
    else:
        layout = [[gui.Text('WSA Sideloader could not install the application. Please check that:\nThe APK file is valid\nWSA is running\nDev mode is enabled and the correct address has been entered')],
                [gui.Exit()]]
        window = gui.Window('Information', layout)

        event, values = window.Read()
        window.Close()