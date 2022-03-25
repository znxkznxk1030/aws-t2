import argparse
import os
import glob


parser = argparse.ArgumentParser('This will rename files')
parser.add_argument('--prefix', '-p', metavar='<prefix>', type=str, nargs='?', default='',
                    help='a prefix for specifying this files')
parser.add_argument('--dir_path', '-d', metavar='<directory path>', type=str, nargs='?', default='./figures',
                    help='a target directory path, default is current directory ./')
parser.add_argument('--postfix', metavar='<postfix>', type=str, nargs='?', default='',
                    help='a postfix for specifying this files')

args = parser.parse_args()
prefix = args.prefix
path = args.dir_path
postfix = args.postfix


def sorted_ls(path):
    def mtime(f): return os.stat(os.path.join(f)).st_mtime
    return list(sorted(glob.glob(path + '/*'), key=mtime))


for i, org_nm in enumerate(sorted_ls(path)):
    dst_fnm = os.path.join(
        path, prefix + '-' + '{0:03d}'.format(i) + postfix + '.png')
    os.rename(org_nm, dst_fnm)
    print(org_nm + ' => ' + dst_fnm)
