import os
from func import *

cont = 1
while cont: 
    os.system("cls");
    info()
    print "1) Create Cute USB Drive"                
    print "2) Disable Auto Run"  
    input = raw_input("Input: ")
    
    if input == "1":
        read_only = raw_input("Make read only (Y/N): ")

        input = raw_input("Enter drive name (eg: D,E,F...): ")

        driveName = win32api.GetVolumeInformation(input + ":\\")[0]
        
        format_drive(input + ":\\", "NTFS", driveName)                

        if read_only == "n" or read_only == "N":  
            public = CreateFolder(input + ":\Put here")
            public.set_public()
            print "**INFO** \"Put here\" folder created for other."

        share = CreateFolder(input + ":\Read from here")
        share.set_share()    
        print "**INFO** \"Read from here\" folder created for puting file so other can read."

        drive_read_only = CreateFolder(input+ ":\\" )
        drive_read_only.set_read_only()
        print "**INFO** Root set to read only."
        
    else:
        try:
            print "Creating registry key."
            key = winreg.CreateKeyEx(
                winreg.HKEY_LOCAL_MACHINE, 
                r'Software\Microsoft\Windows\CurrentVersion\Policies\Explorer', 
                0, 
                winreg.KEY_SET_VALUE)
            print "Setting value"
            winreg.SetValueEx(key, "NoDriveTypeAutoRun", 0, winreg.REG_DWORD, 4)
        except:
            print "Try again with admin priviledge\n"
            raw_input("Press any key to exit.")
            exit()
            
    print "All done"
    
    input = raw_input("Press e to exit: ")
    if input == "e":
        cont = 0