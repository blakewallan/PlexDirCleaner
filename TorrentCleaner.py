__author__ = 'blakeallan'

import os

from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import ttk

root = Tk()
root.withdraw()

# Using send2trash instead of os.remove
import send2trash

# Bloat file extensions, commonly in torrent files, to be deleted
badExtension = ".txt", ".jpg", ".png", ".srt", ".torrent", ".nfo", ".DS_Store"

# Folder location of media stored in a variable using tkinter file browser
filepath = askdirectory()

def countFiles():
    # variables to keep track of file sizes, directory sizes, and size of files to be deleted
    totalScanned = 0
    totalDeleted = 0
    badFileCount = 0

    # Loops through the directory specified and finds files below size limit or ending with bad extension
    # updates count of bad files found, the ammount of files scanned and size of files found
    for root, dirs, files in os.walk(filepath):
        for file in files:
            totalScanned += 1
            toSearch = str(file.title())
            fileSize = (os.path.join(root, file))

            if file.endswith(badExtension) or (
                            (os.path.getsize(fileSize) / 1048576) < 20 and (os.path.getsize(fileSize) / 1048576) > 0.1):
                badFile = (os.path.join(root, file))

                deletedfileSize = os.path.getsize(badFile)

                # Update the total size of bad files
                totalDeleted += deletedfileSize
                badFileCount += 1

        # If bad files add up to more that one GB display using GB
        if round(totalDeleted / 1073741824) > 1:
            totalGbDeleted = round(totalDeleted / 1073741824, 2)
            message = "Found " + str(badFileCount) + " bad files\nTotal storage to cleared: " + str(
                totalGbDeleted) + "Gb"
            return message

        # Else display in MB
        else:
            round(totalDeleted / 1048576)
            totalMbDeleted = round(totalDeleted / 1048576, 2)
            message = "Found " + str(badFileCount) + " bad files\nTotal storage to cleared: " + str(
                totalMbDeleted) + "Mb"
            return message


def deleteFiles():
    countStatus = str(countFiles())
    shouldDelete = tkMessageBox.askquestion("Delete?", countStatus)
    if shouldDelete == "yes":
        for root, dirs, files in os.walk(filepath):
            for file in files:
                fileSize = (os.path.join(root, file))
                if file.endswith(badExtension) or (
                                (os.path.getsize(fileSize) / 1048576) < 30 and (
                                    os.path.getsize(fileSize) / 1048576) > 0.1):
                    badFile = (os.path.join(root, file))
                    send2trash.send2trash(badFile)

        tkMessageBox.showinfo("DONE!", "All files have been deleted. \nThanks for using Torrent Cleaner")

    else:
        quit()

countFiles()
deleteFiles()








