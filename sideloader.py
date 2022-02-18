import dload
import os
import PySimpleGUI as gui
import platform

version = "1.1.0"

def main():
    # Check if OS is Windows 11
    if int((platform.version().split('.')[2])) < 22000:
        layout = [[gui.Text('Sorry! WSA Sideloader will only run on Windows 11.')],
                [gui.Exit()]]
        window = gui.Window('Unsupported OS', layout)

        event, values = window.Read()
        if event is None or "Exit":
            quit()
        window.Close()

    if os.path.isdir('platform-tools') == False: # Check if platform tools present
        layout = [[gui.Text('In order to function correctly, WSA Sideloader will need to download the SDK platform tools.')],
                [gui.Button('Continue')]]
        window = gui.Window('Information', layout)
        event, values = window.Read()
        if event is None:
            quit()
        window.Close()
        layout = [[gui.Text('Downloading SDK platform tools, please wait...')]]
        window = gui.Window('Please wait...', layout,no_titlebar=True,keep_on_top=True)
        event, values = window.Read(timeout=0)
        dload.save_unzip("https://dl.google.com/android/repository/platform-tools-latest-windows.zip",extract_path=os.getcwd(),delete_after=True)
        window.Close()

    layout = [[gui.Text('Choose APK file to install:')],
            [gui.Input(),gui.FileBrowse(file_types=(("APK files","*.apk"),))],
            [gui.Text('ADB address:')],
            [gui.Input('127.0.0.1:58526')],
            [gui.Button('Install'),gui.Button('Installed apps')]]

    window = gui.Window('WSA Sideloader '+version, layout)

    while True:
        event, values = window.Read()
        if event is None:
            quit()
        if event == "Installed apps":
            address = values[1]
            command = os.popen('cmd /c "cd platform-tools & adb connect '+address+' & adb shell am start -n "com.android.settings/.applications.ManageApplications""')
            output = command.readlines()
            check = str(output[len(output)-1])
            if check.startswith("Starting: Intent { cmp=com.android.settings/.applications.ManageApplications }"):
                pass
            else:
                gui.SystemTray.notify('Unable to perform this operation', 'Please check that WSA is running and the correct ADB address has been entered.',display_duration_in_ms=5000,icon=None)
        if event == "Install":
            break

    source_filename = values[0]
    address = values[1]

    window.Close()

    layout = [[gui.Text('Installing application, please wait...')]]
    window = gui.Window('Please wait...', layout,no_titlebar=True,keep_on_top=True)
    event, values = window.Read(timeout=0)
    command = os.popen('cmd /c "cd platform-tools & adb connect '+address+' & adb install '+source_filename+'"')
    output = command.readlines()
    check = str(output[len(output)-1])
    window.Close()
    if check.startswith("Success"):
        layout = [[gui.Text('The application has been successfully installed.')],
                [gui.Exit(),gui.Button('Install another APK')]]
        window = gui.Window('Information', layout)

        event, values = window.Read()
        if event == "Install another APK":
            window.Close()
            main()
        else:
            quit()
    else:
        layout = [[gui.Text('WSA Sideloader could not install the application. Please check that:\nThe APK file is valid\nWSA is running\nDev mode is enabled and the correct address has been entered')],
                [gui.Button('OK')]]
        window = gui.Window('Error', layout)

        event, values = window.Read()
        if event == "OK":
            window.Close()
            main()
        else:
            quit()