""" Utility to print a directory as a tree """

from pathlib import Path

INNER1, INNER2 = '├──', '│   '
LAST1, LAST2 = '└──', '    '


def print_tree(path: Path, prefix: str = '', inner: str = ''):
    if prefix:
        print(prefix + " " + path.name)
    else:
        print(path)

    if path.is_dir():
        items = sorted(
            path.iterdir(),
            key=lambda i: (not i.is_dir(), str(i))
        )
        args = inner + INNER1, inner + INNER2
        while items:
            item = items.pop(0)
            if not items:
                args = inner + LAST1, inner + LAST2
            print_tree(item, *args)
