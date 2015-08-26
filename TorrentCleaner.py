__author__ = 'blakeallan'

import os
from os.path import abspath, expanduser
import send2trash
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

# Bloat file extensions, commonly in torrent files, to be deleted
badExtension = ".txt", ".jpg", ".png", ".srt", ".torrent", ".nfo"

# Folder location of media stored in a variable using tkinter file browser
filepath = filedialog.askdirectory()

print("\nScanning: ", filepath, "\n")

def showScan():

    #variables to keep track of file sizes, directory sizes, and size of files to be deleted
    totalScanned = 0
    totalDeleted = 0
    badFileCount = 1

    for root, dirs, files in os.walk(filepath):
        for file in files:
            totalScanned += 1
            fileSize = (os.path.join(root, file))
            if file.endswith(badExtension) or ((os.path.getsize(fileSize) / 1048576) < 20 and (os.path.getsize(fileSize) / 1048576) > 0.1) :

                badFile = (os.path.join(root, file))

                deletedfileSize = os.path.getsize(badFile)
                
                megabytes = round(deletedfileSize / 1048576, 2)
                gigabytes = round(deletedfileSize / 1073741824, 2)

                print("Found: ", file)
                #Case to print file size in Gb or Mb depending on size
                if gigabytes > 1:
                    print("File Size = ", gigabytes, "Gb\n")
                else:
                    print("File Size = ", megabytes, "Mb\n")

                # Update the total size of bad files
                totalDeleted += deletedfileSize
                badFileCount += 1

                return totalScanned, totalDeleted, badFileCount

print("\nScan Complete")

def totalFound():
    totalDeleted = showScan()[1]
    if round(totalDeleted / 1073741824, 2) > 1:
        totalGbDeleted = round(totalDeleted / 1073741824, 2)
        return "Found ", showScan()[2], " bad files\nTotal storage to cleared: ", totalGbDeleted, "Gb"

    else:
        round(totalDeleted / 1048576, 2)
        totalMbDeleted = round(totalDeleted / 1048576, 2)
        message = "Found ", showScan()[2], " bad files\nTotal storage to cleared: ", totalMbDeleted, "Mb"
        return message

shouldDelete = messagebox.askquestion("Delete?",  totalFound())

if shouldDelete == "yes":
    for root, dirs, files in os.walk(filepath):
        for file in files:
            fileSize = (os.path.join(root, file))
            if file.endswith(badExtension) or ((os.path.getsize(fileSize) / 1048576) < 20 and (os.path.getsize(fileSize) / 1048576) > 0.1) :
                badFile = (os.path.join(root, file))
                send2trash.send2trash(badFile)

    messagebox.showinfo("DONE!", "All files have been deleted. \nThanks for using Torrent Cleaner")

else:
    quit()









