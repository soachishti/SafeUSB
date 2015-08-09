import os, sys
import win32api
import win32security
import ntsecuritycon as con
import _winreg as winreg
from ctypes import *

def info () :
    print "SafeUSB v1.0 (soachishti)"
    print "-> Keep your USB and system safe from viruses."
    print "Note: It is automated script for the instruction given on bit.ly/SafeUSB\n"

class CreateFolder():
    path = ""
    everyone = admin = user = ""
    def __init__(self, fn):       
        self.path = fn
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
        self.everyone, domain, type = win32security.LookupAccountName ("", "Everyone")
        self.admin, domain, type = win32security.LookupAccountName ("", "Administrators")
        self.user, domain, type = win32security.LookupAccountName ("", win32api.GetUserName ())

    def show_cacls (self):
        print 
        for line in os.popen ("cacls %s" % self.path).read ().splitlines ():
            print line
    
    def print_file_info(self):
        show_cacls (self.path)

    def set_public(self) :
        sd = win32security.GetFileSecurity (self.path, win32security.DACL_SECURITY_INFORMATION)
        dacl = win32security.ACL ()
        
        # Everyone read/write
        dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.GENERIC_READ | con.GENERIC_WRITE, self.everyone)  
        
        #This user will have full access
        dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_ALL_ACCESS, self.user)  
          
        sd.SetSecurityDescriptorDacl (1, dacl, 0)
        win32security.SetFileSecurity (self.path, win32security.DACL_SECURITY_INFORMATION, sd)
    
    def set_read_only(self) :
        sd = win32security.GetFileSecurity (self.path, win32security.DACL_SECURITY_INFORMATION)
        dacl = win32security.ACL ()
        
        # Everyone read only
        dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.GENERIC_READ, self.everyone)  

        #This user will have full access
        dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_ALL_ACCESS, self.user) 
        
        sd.SetSecurityDescriptorDacl (1, dacl, 0)
        win32security.SetFileSecurity (self.path, win32security.DACL_SECURITY_INFORMATION, sd)
      
    def set_share(self) :
        sd = win32security.GetFileSecurity (self.path, win32security.DACL_SECURITY_INFORMATION)
        dacl = win32security.ACL ()
        
        # Every one can read only
        dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.GENERIC_READ, self.everyone) 
        
        #This user will have full access
        dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_ALL_ACCESS, self.user)  
          
        sd.SetSecurityDescriptorDacl (1, dacl, 0)
        win32security.SetFileSecurity (self.path, win32security.DACL_SECURITY_INFORMATION, sd)
  
#http://stackoverflow.com/questions/27568706/format-drive-in-python  
def myFmtCallback(command, modifier, arg):
    print("Formatting... -c " + str(command))
    return 1
    
def format_drive(Drive, Format, Title):
    if Drive == 'c' or Drive == 'C':
        raw_input("Not allowed")

        exit(0)

    print Drive + " will be formatted!!!\n" 
    input = raw_input("Are you sure? (Y/N): ")
    if input == 'y' or input == 'Y':
        fm = windll.LoadLibrary('fmifs.dll')
        FMT_CB_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
        FMIFS_REMOVEABLEDISK = 0x0B
        fm.FormatEx(c_wchar_p(Drive), FMIFS_REMOVEABLEDISK, c_wchar_p(Format), c_wchar_p(Title), True, c_int(0), FMT_CB_FUNC(myFmtCallback))
    else:
        exit()

cont = 1
while cont: 
    os.system("cls");
    info()
    print "1) Create Cute USB Drive\n"                
    print "2) Disable Auto Run\n"  
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