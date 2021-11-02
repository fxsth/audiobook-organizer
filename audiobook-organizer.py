import sys
import tagger
import splitter
import ntpath
import os
from metadata import Audiobookmeta
import argparse

def fixInputDirectory(inputDirectory):
    inputDirectory = inputDirectory.strip()
    if (inputDirectory.startswith('.\\')):
        inputDirectory = inputDirectory[2:]
    if (inputDirectory.endswith('\\')):
        inputDirectory = inputDirectory[:-2]
    return inputDirectory

print("starting audiobook-organizer")
parser = argparse.ArgumentParser(description='converts, splits, renames and tags audiobooks.')
parser.add_argument("-i", "--inputdir", type=str, required=True, help='directory of audiobook input files')
parser.add_argument("-t", "--searchterm", type=str, help='<author - title> for metatag search and ouput as author/title/file.mp3')
parser.add_argument("-o", "--outputdir", type=str, help='directory of audiobook output files')
parser.add_argument("-n", "--no-split", dest='split', action='store_false', help='does NOT split files')
parser.set_defaults(split=True)
parser.add_argument("-r", "--recursive", dest='recursive', default=False, action='store_true', help='searches for files in inputdir recursively')

args = parser.parse_args()
print(args)


dir = fixInputDirectory(args.inputdir)
recursive = args.recursive
split = args.split
# default directory is home
if( not os.path.exists(dir)):
    home = os.path.expanduser("~")
    dir = home + "/" + dir
searchterm = ntpath.basename(dir)
# special case: inputdir is only file
if(os.path.isfile(args.inputdir)):
    dir = args.inputdir
    searchterm = ntpath.basename(dir).split('.')[0]
if(args.searchterm is not None):
    searchterm = args.searchterm

title = searchterm
if("-" in searchterm):
    author = searchterm.split("-")[0]
    title = searchterm.split("-")[-1]
    print("author: " + author, " title: " + title)
    outputDir = dir + "/" + author + "/" + title
else:
    outputDir = dir + "/" + searchterm
# Load Metadata
audiobookmeta = Audiobookmeta(searchterm)
metadataFound = audiobookmeta.tryRetrieveFromITunes()
if(args.outputdir is not None):
    outputDir = args.outputdir+"/"+author+"/"+title
outputDir = outputDir.replace(" / ", "/")
# Create Output Directory
splitter.create_dir(outputDir)
# Split Files In Segments If Necessary and put them in output dir
splitter.splitIfNecessary(dir, outputDir, title, split, recursive)
# Rename Files
splitter.renameAllFilesInDirectory(outputDir, title)
# Tag All Files With Loaded Metadata
tagger.tagAllInDirectory(outputDir, audiobookmeta)

print("End")
