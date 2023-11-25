# xclean

File de-duplication utility

    usage: xclean [-h] [-m MAIN] [-t TARGET] [-a ARCHIVE_TO] [-e [EXTENSIONS ...]] [--remove] [--trash] [--clean]

    options:
      -h, --help            show this help message and exit
      -m MAIN, --main MAIN
                            Directory where master files reside
      -t TARGET, --target TARGET
                            Directory where duplicate files may reside
      -a ARCHIVE_TO, --archive-to ARCHIVE_TO
                            Archive duplicates to folder
      -e [EXTENSIONS ...], --extensions [EXTENSIONS ...]
                            Extensions
      --remove              Remove duplicate files
      --trash               Trash duplicate files
      --clean               Clean database
