import os
import sys

def resource_path(relative):
  #print(os.environ)
  application_path = os.path.abspath(".")
  if getattr(sys, 'frozen', False):
      # If the application is run as a bundle, the pyInstaller bootloader
      # extends the sys module by a flag frozen=True and sets the app 
      # path into variable _MEIPASS'.
      application_path = sys._MEIPASS
  #print(application_path)
  return os.path.join(application_path, relative)