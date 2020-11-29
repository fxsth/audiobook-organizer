# audiobook-organizer
audiobook-organizer is a tool to split, rename and tag audiobooks. Splits into 30min mp3 files, if larger. Tagging works automatically with the first result in iTunes search.

`audiobook-organizer.py "/path/to/audiobookfiles" "author - book title" "/path/to/outputdirectory"`

Sets all files in input directory as input and create the new audiobook output files in a folder outputdirectory/author/audiobook.
Input directory argument is mandatory, search term and output directory arguments are optional. If only the input directory is specified, it will search for the folder name as search term. Output directory would be the same as input directory.

Tags set are title, artist, album, albumartist, track number, genre, year, as well as the cover in 600x600px.