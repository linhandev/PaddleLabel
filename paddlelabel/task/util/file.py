import os
import os.path as osp
import shutil
from pathlib import Path


# TODO: switch to pathlib

image_extensions = [".bmp", ".jpg", ".jpeg", ".png", ".gif", ".webp"]


def ensure_unique_base_name(paths):
    """Ensure all paths have unique base name, will change file name on disk

    Args:
        paths (str): Full paths
    """

    all_names = set()
    curr_names = set()
    changed_list = []
    paths = [Path(p) for p in paths]

    for path in paths:
        all_names.add(path.name.split(".")[0])

    for path in paths:
        basename = path.name.split(".")[0]
        if basename in curr_names:  # duplicate
            idx = 1
            while f"{basename}-{idx}" in all_names:
                idx += 1
            new_path = path.parent / Path(f"{basename}-{idx}{path.name[len(basename):]}")
            path.rename(new_path)
            all_names.add(new_path.name)
            curr_names.add(new_path.name)
            changed_list.append((path, new_path))
        else:
            curr_names.add(basename)

    return changed_list


def create_dir(path):
    if path is None:
        raise RuntimeError("Path to create is None")
    if not osp.isabs(path):
        raise RuntimeError(f"Only supports absolute path, got {path}")
    os.makedirs(path, exist_ok=True)


def remove_dir(path):
    if not osp.exists(path):
        return
    shutil.rmtree(path)


def listdir(folder, filters={"exclude_prefix": ["."]}):
    """
    return relative path of all files satisfying filters under the folder and its subfolders

    Args:
        folder (str): the folder to list
        filters (dict, optional): Four lists, include/exclude_prefix/postfix. Include first, satisfying either include, then exclude fail either one gets excluded.

    Returns:
        list: File paths relative to folder, sorted
    """

    files = []
    for root, fdrs, fs in os.walk(folder):
        if osp.basename(root).startswith("."):  # skip all hidden folders
            continue
        for f in fs:
            # files.append(osp.normpath(osp.join(root, f)))
            files.append(osp.join(root, f))
    files = [osp.relpath(f, folder) for f in files]
    # TODO: support regx
    include_prefix = filters.get("include_prefix", [])
    include_postfix = filters.get("include_postfix", [])

    def include(path):
        f = osp.basename(path)
        for pref in include_prefix:
            if f[: len(pref)].lower() == pref:
                return True
        for postf in include_postfix:
            if f[-len(postf) :].lower() == postf:
                return True
        return False

    if len(include_prefix) != 0 or len(include_postfix) != 0:
        files = list(filter(include, files))

    exclude_prefix = filters.get("exclude_prefix", [])
    exclude_postfix = filters.get("exclude_postfix", [])

    def exclude(path):
        f = osp.basename(path)
        for pref in exclude_prefix:
            if f[: len(pref)] == pref:
                return False
        for postf in exclude_postfix:
            if f[-len(postf) :] == postf:
                return False
        return True

    files = list(filter(exclude, files))
    files.sort(key=osp.basename)
    # files = [osp.normpath(p) for p in files]
    return files


def copy(src, dst, make_dir=False):
    # src = osp.normpath(src)
    # dst = osp.normpath(dst)
    if dst == osp.dirname(src) or src == dst:
        return
    if make_dir:
        os.makedirs(osp.dirname(dst), exist_ok=True)
    shutil.copy(src, dst)


def copycontent(src, dst):
    """
    Recursively copy everything in src to dst. Create dst if not exist.

    Args:
        src (str): source folder
        dst (str): destination folder
    """

    assert osp.abspath(src), f"src dir {src} isn't abspath"
    assert osp.abspath(dst), f"dst dir {dst} isn't abspath"
    assert src != dst, f"The source and destination folder are both {src}"

    for root, fdrs, fs in os.walk(src):
        if osp.basename(root).startswith("."):  # skip all hidden folders
            continue
        if not osp.exists(osp.join(dst, osp.relpath(root, src))):
            os.makedirs(osp.join(dst, osp.relpath(root, src)))

        for f in fs:
            fsrc = osp.join(root, f)
            fdst = osp.join(osp.join(dst, osp.relpath(root, src), f))
            if osp.exists(fdst):
                continue
            copy(fsrc, fdst)


def expand_home(path):
    if path[0] == "~":
        path = osp.join(osp.expanduser("~"), path[2:])
    return path


def get_fname(path: str):
    """get file name from a windows or linux path"""
    return path.split("\\")[-1].split("/")[-1]
