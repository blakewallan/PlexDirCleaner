__author__ = 'blakeallan'

import os

from Tkinter import *
from tkFileDialog import *
import tkMessageBox
import ttk

root = Tk()
root.withdraw()

# import imdb
from imdb import *
import imdb.helpers

# Using send2trash instead of os.remove
import send2trash

# Module searches Bing with registered APPID and returns specified amount of results
from bingpy import WebSearch

# Bloat file extensions, commonly in torrent files, to be deleted
badExtension = ".txt", ".jpg", ".png", ".srt", ".torrent", ".nfo", ".DS_Store"

crapFileStrings = ["1080p", "brrip", "720p", "yify", "rargb", "web-dl", "bluray", "hdrip", "dvdscr", "hd", "hdtv", "hc",
                   "rip", "x264", "dvdrip", "avi", "mp4", "mkv", "mpeg"]

# Folder location of media stored in a variable using tkinter file browser
filepath = askdirectory()

# Access to the IMDB library
imdbAccess = IMDb()
ia = IMDb('http')

# Function compares modified file title against a list of unnaceptable crap file strings often included in torrent DL's
def badWords(wordList, movieTitle):
    return set(wordList).intersection(movieTitle.split())


# Function strips periods from file names, and stores just the first four words to avoid junk in the name
#Then uses google search to retreive the imdb URL by adding "site: imdb.com" to the end of the search
#Then uses the imdb url to retreive the movies title using get_byURL
def renameFiles():
    for root, dirs, files in os.walk(filepath):
        for file in files:

            strip = str((file.replace(".", " ")))
            shortURL = str(strip.split()[:4]).replace("[", "").replace("'", "").replace(",", "").replace("]", "")
            shortURL = str.lower(shortURL)

            if badWords(crapFileStrings, shortURL):
                for word in badWords(crapFileStrings, shortURL):
                    shortURL = shortURL.replace(word, "")

            p = ttk.Progressbar(mode='determinate')
            p.update_idletasks()

            web = WebSearch("0wYsR23LZOF46/s1Nzolb+9sxjN4wIkeYA7rfNUpaDg")
            pages = web.search(shortURL + " site:imdb.com", 1)
            for page in pages:
                newFileName = str(imdb.helpers.get_byURL(page.url))

            print(shortURL)
            print(newFileName)


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
        if round(totalDeleted / 1073741824, 2) > 1:
            totalGbDeleted = round(totalDeleted / 1073741824, 2)
            message = "Found " + str(badFileCount) + " bad files\nTotal storage to cleared: " + str(
                totalGbDeleted) + "Gb"

        # Else display in MB
        else:
            round(totalDeleted / 1048576, 2)
            totalMbDeleted = round(totalDeleted / 1048576, 2)
            message = "Found " + str(badFileCount) + " bad files\nTotal storage to cleared: " + str(
                totalMbDeleted) + "Mb"

        # Return the status of the files
        return message


def deleteFiles():
    shouldDelete = tkMessageBox.askquestion("Delete?", countFiles())
    if shouldDelete == "yes":
        for root, dirs, files in os.walk(filepath):
            for file in files:
                fileSize = (os.path.join(root, file))
                if file.endswith(badExtension) or (
                                (os.path.getsize(fileSize) / 1048576) < 20 and (
                                    os.path.getsize(fileSize) / 1048576) > 0.1):
                    badFile = (os.path.join(root, file))
                    send2trash.send2trash(badFile)

        tkMessageBox.showinfo("DONE!", "All files have been deleted. \nThanks for using Torrent Cleaner")

    else:
        quit()


renameFiles()
countFiles()
deleteFiles()








