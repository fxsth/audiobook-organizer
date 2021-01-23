import sys
import tagger
import splitter
import ntpath
import os
from metadata import Audiobookmeta
import argparse

print("starting audiobook-organizer")
parser = argparse.ArgumentParser(description='converts, splits, renames and tags audiobooks.')
parser.add_argument("-i", "--inputdir", type=str, required=True, help='directory of audiobook input files')
parser.add_argument("-t", "--searchterm", type=str, help='<author - title> for metatag search and ouput as author/title/file.mp3')
parser.add_argument("-o", "--outputdir", type=str, help='directory of audiobook output files')

# parser.add_argument("-i", "--inputdir",dest="inputdir", type=str, nargs='2',
#                     help='directory of audiobook input files', metavar=("ref","rmsd"))
# parser.add_argument('-t','--searchterm', type=str,
#                     help='author - book title')
# parser.add_argument('-o','--outputdir', type=str, nargs='2',
#                     help='directory of audiobook output files')
args = parser.parse_args()
print(args)
dir = args.inputdir
# default directory is home
if( not os.path.exists(dir)):
    home = os.path.expanduser("~")
    dir = home + "/" + dir
searchterm = ntpath.basename(dir)
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
# Split Files In Segments If Necessary
splitter.splitIfNecessary(dir, outputDir, title)
# Rename Files
splitter.renameAllAfterSplitting(outputDir, title)
# Tag All Files With Loaded Metadata

tagger.tagAllInDirectory(outputDir, audiobookmeta)

print("End")