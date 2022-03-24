import os
import shutil
import glob

path = "./figures"

def sorted_ls(path):
    def mtime(f): return os.stat(os.path.join(f)).st_mtime
    return list(sorted(glob.glob(path + '/*'), key=mtime))


for i, file_name in enumerate(sorted_ls(path)):
    print(file_name)
    os.rename(file_name, os.path.join(
        path, 'rdb-' + '{0:03d}'.format(i) + '.png'))
    print(file_name)
