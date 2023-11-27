""" main.py

tree-diff takes two directories and compares structure and files
"""
import argparse
import hashlib
import math
from collections import defaultdict
from pathlib import Path
from termcolor import colored
import colorama

from typing import Tuple, Any
from argparse import Namespace, ArgumentParser

# Just windows things
colorama.init()


def main() -> None:
    args, parser = parse_arguments()
    verify_args(args, parser)

    comparison = compare_directories(args.directory1, args.directory2, args.contents)
    print_tree_style(Path(args.directory2), comparison, args.color)


def parse_arguments() -> Tuple[Namespace, ArgumentParser]:
    parser = argparse.ArgumentParser(
                    prog='tree-diff',
                    description='Compute changes between two relative directory structures',
                    epilog='')
    parser.add_argument('directory1')           # positional argument
    parser.add_argument('directory2')           # positional argument
    parser.add_argument('-c', '--color', action='store_true', default=False,
                        help='Whether to render output with color')     
    parser.add_argument('-s', '--stat',
                        action='store_true',
                        help='Toggle looking at file metadata (created, changed, etc)')
    parser.add_argument('-x', '--contents',
                        action='store_true',
                        help='Toggle looking at contents of file')
    args = parser.parse_args()
    return args, parser


def verify_args(args: Namespace, parser: ArgumentParser) -> None:
    p1 = Path(args.directory1)
    p2 = Path(args.directory2)
    if not p1.exists():
        print(f'[x] First directory {p1.absolute()} was not a valid/existing path.')
        exit(1)  # 1 input directory does not exist
    if not p2.exists():
        print(f'[x] First directory {p2.absolute()} was not a valid/existing path.')
        exit(1)  # 1 input directory does not exist


def get_files_and_folders(root_dir):
    """ Walk through the directory and return a set of file and folder paths.
    """
    root_path = Path(root_dir)
    all_files = set()
    for path in root_path.rglob('*'):  # rglob('*') returns all files and folders recursively
        all_files.add(path.relative_to(root_path).as_posix())
    return all_files


def get_file_hash(file_path):
    """ Compute SHA256 hash of a file. """
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def compare_directories(dir1, dir2, w_hash: bool):
    """ Compare two directories and return a dict with added and removed files. """
    files_dir1 = get_files_and_folders(dir1)
    files_dir2 = get_files_and_folders(dir2)

    added = files_dir2 - files_dir1
    removed_files = files_dir1 - files_dir2
    changed = {}

    removed = defaultdict(list)
    for file_path in removed_files:
        directory = Path(file_path).parent
        removed[directory.as_posix()].append(file_path)

    if w_hash:
        # Check for changed files
        common_files = files_dir1.intersection(files_dir2)
        for file in common_files:
            file1 = Path(dir1) / file
            file2 = Path(dir2) / file

            if file1.is_file() and file2.is_file():
                hash1 = get_file_hash(file1)
                hash2 = get_file_hash(file2)

                if hash1 != hash2:
                    changed[file] = (file1.stat().st_size, file2.stat().st_size)

    return {'added': added, 'removed': removed, 'changed': changed}


def print_tree_style(dir2, comparison, colorful : bool = False):
    """ Print the directory structure in a tree style, including nesting level.
    """

    def status(path: str) -> str:
        path = Path(path).relative_to(dir2).as_posix()
        _status = ""
        if path in comparison['added']:
            _status = "[+]"
        elif path in comparison['removed']:
            _status = "[-]"
        elif path in comparison['changed']:
            _status = "[~]"
        return _status

    def print_tree(directory, prefix=''):
        """
        Print the tree structure for the specified directory using pathlib.
        """

        # Get all path objects in the current directory
        entries = list(directory.iterdir())
        entries.sort(key=lambda x: (x.is_file(), x.name.lower()))

        for i, entry in enumerate(entries):
            delta = status(entry.as_posix())  # [+] [-]
            connector = '└── ' if i == len(entries) - 1 else '├── '

            if i == 0:  # At starting point
                if Path(directory).relative_to(dir2).as_posix() in comparison['removed']:
                    for _file in comparison['removed'][Path(directory).relative_to(dir2).as_posix()]:
                        text = f"{prefix}{connector}{'[-]'}{Path(_file).name}"
                        if colorful:
                            print(colored(text, "red"))
                        else:
                            print(text)

            if entry.is_dir():
                # Print directory name
                print(f"{prefix}{connector}{delta}{entry.name}")
                # Recurse into the directory
                new_prefix = prefix + ('    ' if i == len(entries) - 1 else '│   ')
                print_tree(entry, new_prefix)
            else:
                # Print file name
                text = f"{prefix}{connector}{delta}{entry.name}"
                if colorful:
                    #  attrs=["reverse", "blink"]
                    if delta == '[+]':
                        print(colored(text, "green"))
                    elif delta == '[-]':
                        print(colored(text, "red"))
                    elif delta == '[~]':
                        sizes = comparison['changed'][Path(entry).relative_to(dir2).as_posix()]
                        text += f'  ({convert_size(sizes[0])} -> {convert_size(sizes[1])})'
                        print(colored(text, "yellow"))
                    else:
                        print(text)
                else:
                    if delta == '[~]':
                        sizes = comparison['changed'][Path(entry).relative_to(dir2).as_posix()]
                        text += f'  ({convert_size(sizes[0])} -> {convert_size(sizes[1])})'
                    print(text)
            
    print_tree(dir2)


def convert_size(size_bytes):
    """
    Convert a file size from bytes to a human-readable format.
    """
    if size_bytes == 0:
        return "0B"
    size_names = ("b", "kb", "mb", "gb", "tb")  # , "PB", "EB", "ZB", "YB") At this point, the problem wasn't actually worth it.
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = int(size_bytes // p)
    return f"{s}{size_names[i]}"

if __name__ == "__main__":
    main()