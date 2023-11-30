from argparse import ArgumentParser
from xclean.scanner import Scanner


def main():
    parser = ArgumentParser(description='File de-duplication utility')
    parser.add_argument('-m', '--main', help='Directory where main files reside')
    parser.add_argument('-t', '--target', help='Directory where duplicate files may reside')
    parser.add_argument('-a', '--archive-to', help='Archive duplicates to directory')
    parser.add_argument('-e', '--extensions', nargs='*', help='Extensions')
    parser.add_argument('--remove', default=False, action='store_true', help='Remove duplicate files')
    parser.add_argument('--trash', default=False, action='store_true', help='Trash duplicate files')
    parser.add_argument('--clean', default=False, action='store_true', help='Clean database')
    parser.add_argument('--xmp', default=False, action='store_true', help='Include xmp files when checking for duplicates')
    args = parser.parse_args()
    xclean = Scanner(db_path='xclean.sqlite', clean=args.clean)
    if args.main is not None:
        xclean.scan(
            dir_path=args.main, extensions=args.extensions
        )
    if args.target is not None:
        xclean.clean(
            dir_path=args.target, extensions=args.extensions,
            remove_dups=args.remove, trash_dups=args.trash,
            check_xmp=args.xmp,
            archive_to=args.archive_to
        )
