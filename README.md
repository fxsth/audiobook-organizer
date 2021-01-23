# audiobook-organizer
audiobook-organizer is a tool to split, rename and tag audiobooks. Splits into 60min mp3 files, if larger than 100mb. Tagging works automatically with the first result in iTunes search.
The tool supports the recommended naming standard of Plex.

`audiobook-organizer.py "/path/to/audiobookfiles" "author - book title" "/path/to/outputdirectory"`
```
usage: audiobook-organizer.py [-h] -i INPUTDIR [-t SEARCHTERM] [-o OUTPUTDIR]
                              [-r]

converts, splits, renames and tags audiobooks.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTDIR, --inputdir INPUTDIR
                        directory of audiobook input files
  -t SEARCHTERM, --searchterm SEARCHTERM
                        <author - title> for metatag search and ouput as
                        author/title/file.mp3
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        directory of audiobook output files
  -r, --recursive       searches for files in inputdir recursively
```
Sets all files in input directory as input and create the new audiobook output files in a folder outputdirectory/author/audiobook.
Input directory argument is mandatory, search term and output directory arguments are optional. If only the input directory is specified, it will search for the folder name as search term. Output directory would be the same as input directory.

Manipulated tags are title, artist, album, albumartist, track number, genre, year, as well as the cover in 600x600px.

## Requirements

depends on packages:
- ffmpeg-python
- eyed3
    
