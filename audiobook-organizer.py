import sys
import tagger
import splitter
import ntpath
from metadata import Audiobookmeta

if(len(sys.argv)<2):
    print("audiobook-organizer needs the directory of the audiobook as first argument")
    print("Optional second argument: \"Author - Title\"")
    print("Without second argument search term is set to folder name")
    print("Optional third argument is Output directory such that OutputDirectory/author/audiobook")
    print("For example: audiobook-organizer.py \"/path/to/audiobook files\" \"J.K. Rowling - Harry Potter und der Stein der Weisen\"")

    exit()
dir = sys.argv[1]
# dir = "/home/felix/Cornelia Funke/Cornelia Funke - Tintenherz"
searchterm = ntpath.basename(dir)
if(len(sys.argv)==3):
    searchterm = sys.argv[2]
author = searchterm.split("-")[0]
title = searchterm.split("-")[-1]
print("author: " + author, " title: " + title)
# Load Metadata
audiobookmeta = Audiobookmeta(searchterm)
metadataFound = audiobookmeta.tryRetrieveFromITunes()
outputDir = dir+"/"+author+"/"+title
if(len(sys.argv)==4):
    outputDir = sys.argv[3]+"/"+author+"/"+title
outputDir = outputDir.replace(" / ", "/")
# Create Output Directory
splitter.create_dir(outputDir)
# Split Files In Segments If Necessary
splitter.splitIfNecessary(dir, outputDir, title)
# Rename Files
splitter.renameAllAfterSplitting(outputDir, title)
# Tag All Files With Loaded Metadata
tagger.tagAllInDirectory(outputDir, audiobookmeta)
print("End")