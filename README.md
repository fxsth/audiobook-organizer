# audiobook-organizer
audiobook-organizer is a tool to split, rename and tag audiobooks. Tagging works automatically with the first result in iTunes search.

`audiobook-organizer.py "/path/to/audiobookfiles" "author - book title" "/path/to/outputdirectory"`

It will create the new audiobook files in a folder outputdirectory/author/audiobook.
Input file argument is mandatory, search term and output directory arguments are optional. If only the input directory is specified, it will search for the folder name as search term. Output directory would be the same as input directory. 