""" Utility to locate python modules """

import sys
import importlib.util

from pathlib import Path

from .dirtree import print_tree


def search_path(*patterns):
    """ first file/folder in python path that matches any of the patterns """

    for folder in sys.path:
        folder = Path(folder)
        if not folder.is_dir():
            continue
        for file in Path(folder).iterdir():
            if any(file.match(pattern) for pattern in patterns):
                return file

    return None


def search_path_hook(name: str):
    return search_path(f"{name}.pth", f"{name}-*.pth", f"__editable__.{name}-*.pth")


def search_dist_infp(name: str):
    return search_path(f"{name}-*.dist-info")


def where_module(name, tree=False):
    """ locates and displays module location/contents """

    name = name.replace("-", "_")

    spec = importlib.util.find_spec(name)

    if not spec:
        print("%s not found!" % name)
        return None

    if tree and spec.submodule_search_locations:
        for path in spec.submodule_search_locations:
            path = Path(path)
            print_tree(path)

    elif spec.origin:
        file = Path(spec.origin)
        print(file)

    return spec
