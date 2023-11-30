# python setup.py clean --all build_ext --build-lib win
# python -m build -wno dist


# packages=find_packages(exclude=['dev*', 'home*']),
# package_data={"": ["*.pyd", "*.so"]},
# include_package_data=True,


# from build.__main__ import main
# import sys

# main(sys.argv[1:], 'python -m build')

import argparse
import os
import sys

from Cython.Build import cythonize
from setuptools import setup


def collect(path: str = sys.argv[1]):
    modules = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.startswith('__init__'):
                continue
            filepath = os.path.join(dirpath, filename)
            if filepath.endswith('py') and 'kernel_utils' not in filepath:
                # print(filepath)
                modules.append(filepath)

    return modules


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'srcdir',
        type=str,
        nargs='?',
        default='src',
        help='source directory (defaults to current directory)',
    )
    parser.add_argument(
        '--outdir',
        '-o',
        type=str,
        help=f'output directory (defaults to {{srcdir}}{os.sep}dist)',
        metavar='PATH',
    )
    args = parser.parse_args()
    print(args)

    outdir = '.' if not args.outdir else args.outdir

    setup(ext_modules=cythonize(module_list=collect(args.srcdir),
                                exclude=[],
                                build_dir=f"build/src"),
          # 'bdist_wheel','--python-tag=cp3','--plat-name=win-amd64'], # sys.argv[1:]
          script_args=['clean', '--all', 'build_ext',
                       '-b', outdir, '-t', 'build/temp'],
          )
