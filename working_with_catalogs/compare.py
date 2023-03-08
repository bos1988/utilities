import filecmp

 
def report_partial(dcmp): # Print a report on the differences between a and b
    # Output format is purposely lousy
    flags = [
        bool(dcmp.left_only),
        bool(dcmp.right_only),
        bool(dcmp.diff_files),
        bool(dcmp.funny_files),
        bool(dcmp.common_funny)
    ]
    res = ''
    if any(flags):
        res += '-'*50 + '\n'
        res += f'''<<<    {dcmp.left}
>>>    {dcmp.right}

'''
    if dcmp.left_only:
        dcmp.left_only.sort()
        lst = "\n      ".join(dcmp.left_only)
        res += f'''  Only in <<< {dcmp.left} :

      {lst}

'''
    if dcmp.right_only:
        dcmp.right_only.sort()
        lst = "\n      ".join(dcmp.right_only)
        res += f'''  Only in >>> {dcmp.right} :

      {lst}

'''
#     if dcmp.same_files:
#         dcmp.same_files.sort()
#         print('Identical files :', dcmp.same_files)
    if dcmp.diff_files:
        dcmp.diff_files.sort()
        lst = "\n      ".join(dcmp.diff_files)
        res += f'''  Differing files :

      {lst}

'''
    if dcmp.funny_files:
        dcmp.funny_files.sort()
        lst = "\n      ".join(dcmp.funny_files)
        res += f'''  Trouble with common files :

      {lst}

'''
#     if dcmp.common_dirs:
#         dcmp.common_dirs.sort()
#         print('Common subdirectories :', dcmp.common_dirs)
    if dcmp.common_funny:
        dcmp.common_funny.sort()
        lst = "\n      ".join(dcmp.common_funny)
        res += f'''  Common funny cases :

      {lst}

'''

    return res


def report_diff(dcmp): # Report on self and subdirs recursively
#     dcmp.report()
    result = report_partial(dcmp)
    for sd in dcmp.subdirs.values():
        result += report_diff(sd)
    
    return result



dir1 = input('Enter LEFT  path: ')
dir2 = input('Enter RIGHT path: ')

dirs_cmp = filecmp.dircmp(dir1, dir2)

res = report_diff(dirs_cmp)
with open('log.txt', 'w') as f:
    print(res, file=f)
print(res)


input('Press Enter to exit')