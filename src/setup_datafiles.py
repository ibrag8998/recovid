#!/usr/bin/env python3
import os

from cf import get_cf


def setup_datafiles():
    files = get_cf('files')

    try:
        os.makedirs(files.datafiles_dir)
    except OSError:
        print(
            f"{files.datafiles_dir} already exists, no need to overwrite ...")
        return

    os.chdir(files.datafiles_dir)
    os.system(f'touch {files.data} {files.chats} {files.offset}')


if __name__ == "__main__":
    setup_datafiles()
