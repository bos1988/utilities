# -*- coding: utf-8 -*-
import filecmp


def report_partial(dcmp):
    """Report on the differences between dir1 and dir2

    Parameters
    ----------
    dcmp: filecmp.dircmp
        The dircmp object

    Returns
    -------
    res: str
        Comparison result between dir1 and dir1.
    """
    flags = [
        bool(dcmp.left_only),
        bool(dcmp.right_only),
        bool(dcmp.diff_files),
        bool(dcmp.funny_files),
        bool(dcmp.common_funny),
    ]
    result = ""
    if any(flags):
        result += "-" * 50 + "\n"
        result += f"""<<<    {dcmp.left}
>>>    {dcmp.right}

"""
    if dcmp.left_only:
        dcmp.left_only.sort()
        lst = "\n      ".join(dcmp.left_only)
        result += f"""  Only in <<< {dcmp.left} :

      {lst}

"""
    if dcmp.right_only:
        dcmp.right_only.sort()
        lst = "\n      ".join(dcmp.right_only)
        result += f"""  Only in >>> {dcmp.right} :

      {lst}

"""
    #     if dcmp.same_files:
    #         dcmp.same_files.sort()
    #         print('Identical files :', dcmp.same_files)
    if dcmp.diff_files:
        dcmp.diff_files.sort()
        lst = "\n      ".join(dcmp.diff_files)
        result += f"""  Differing files :

      {lst}

"""
    if dcmp.funny_files:
        dcmp.funny_files.sort()
        lst = "\n      ".join(dcmp.funny_files)
        result += f"""  Trouble with common files :

      {lst}

"""
    #     if dcmp.common_dirs:
    #         dcmp.common_dirs.sort()
    #         print('Common subdirectories :', dcmp.common_dirs)
    if dcmp.common_funny:
        dcmp.common_funny.sort()
        lst = "\n      ".join(dcmp.common_funny)
        result += f"""  Common funny cases :

      {lst}

"""
    return result


def report_diff(dcmp):
    """Report on self and subdirs recursively

    Parameters
    ----------
    dcmp: filecmp.dircmp
        The dircmp object

    Returns
    -------
    res: str
        Comparison result between dir1 and dir1 and common subdirectories (recursively).
    """
    result = report_partial(dcmp)
    for sd in dcmp.subdirs.values():
        result += report_diff(sd)

    return result


if __name__ == "__main__":
    dir1 = input("Enter LEFT  path: ")
    dir2 = input("Enter RIGHT path: ")

    dirs_cmp = filecmp.dircmp(dir1, dir2)
    res = report_diff(dirs_cmp)

    with open("log.txt", "w") as f:
        print(res, file=f)
    print(res)

    input("Press Enter to exit")
