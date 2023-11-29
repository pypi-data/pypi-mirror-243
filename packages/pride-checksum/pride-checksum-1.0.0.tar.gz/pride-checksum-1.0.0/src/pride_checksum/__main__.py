import hashlib
import os
import re
import stat
import sys
from pathlib import Path

import click as click


def sha1sum(filename):
    with open(filename, 'rb', buffering=0) as f:
        return hashlib.file_digest(f, 'sha1').hexdigest()


def is_hidden_file(filepath):
    if os.name == 'nt':
        return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    else:
        return Path(filepath).name.startswith('.')


def exit_with_error(code: int):
    print("Exiting.. Please check above errors")
    sys.exit(code)


@click.command()
@click.option('--files_dir', type=click.Path(), required=False,
              help="Checksum will be computed for all the files in this directory")
@click.option('--files_list_path', type=click.Path(), required=False,
              help="Path of the file that contains list of all files whose Checksum should be computed")
@click.option('--out_path', type=click.Path(), required=True, help="Path to save the computed checksum.txt file")
def main(files_dir, files_list_path, out_path):
    if not os.path.isdir(out_path):
        print("[ERROR] Output directory doesn't exist:", out_path)
        exit_with_error(1)

    checksum_file = os.path.join(out_path, "checksum.txt")
    if os.path.exists(checksum_file):
        print("[WARN] checksum.txt already exists in path:", out_path, "This will be overwritten.")
        # yes_no = input("Do you want to overwrite checksum.txt? [y/n]:")
        # if str(yes_no).upper() != 'Y':
        #     print("Exiting...")
        #     sys.exit(0)

    try:
        cfile = open(checksum_file, 'w')
        cfile.write('# SHA-1 Checksum \n')
        cfile.close()
    except PermissionError as e:
        print("[ERROR] No permissions to write to:", checksum_file)
        exit_with_error(1)

    f_list = []
    if files_dir is None and files_list_path is None:
        print("[ERROR] Either dir option or list option should be specified")
        exit_with_error(1)

    if files_dir is not None:
        if not os.path.isdir(files_dir):
            print("[ERROR] Directory doesn't exist: " + files_dir)
            exit_with_error(1)
        else:
            dir_list = os.listdir(files_dir)
            for file_name in dir_list:
                if file_name == 'checksum.txt':
                    continue
                full_file_name = os.path.join(files_dir, file_name)
                if os.path.isdir(full_file_name) and not is_hidden_file(full_file_name):
                    print("[ERROR] Directories are not allowed: " + file_name)
                    exit_with_error(1)
                if os.path.isfile(full_file_name) and bool(re.search('[^-_.A-Za-z0-9]', file_name)):
                    print("[ERROR] invalid filename (only underscore and hyphen special chars are allowed):", file_name)
                    exit_with_error(1)
                if not is_hidden_file(full_file_name):
                    f_list.append(full_file_name)

    if files_list_path is not None:
        if not os.path.isfile(files_list_path):
            print("[ERROR] File doesn't exist: " + files_list_path)
            exit_with_error(1)
        else:
            file_names = []
            dup_files = []
            with open(files_list_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not os.path.isfile(line):
                        if os.path.isdir(line):
                            print("[ERROR] Directories are not allowed: " + line)
                        else:
                            print("[ERROR] File doesn't exist: " + line)
                        exit_with_error(1)
                    elif is_hidden_file(line):
                        print("[ERROR] Hidden files are not allowed: " + line)
                        exit_with_error(1)
                    else:
                        f_list.append(line)
                        file_name = Path(line).name
                        if bool(re.search('[^-_.A-Za-z0-9]', file_name)):
                            print("[ERROR] invalid filename (only underscore and hyphen special chars are allowed):", file_name)
                            exit_with_error(1)
                        if file_name in file_names:
                            dup_files.append(file_name)
                        else:
                            file_names.append(file_name)

            if len(dup_files) > 0:
                print("[ERROR] Following files have duplicate entries:", dup_files)
                exit_with_error(1)
    i = 0
    for f in f_list:
        i = i+1
        print("[", i, "/", len(f_list), "] Processing:", f)
        if os.path.isfile(f):
            sha1_sum = sha1sum(f)
            cfile = open(checksum_file, 'a')
            file_name = Path(f).name
            cfile.write(file_name + '\t' + sha1_sum + '\n')
            cfile.close()

    out_path = Path(checksum_file).parent.resolve()
    print("checksum.txt file has been stored in path:", out_path)


if __name__ == '__main__':
    main()
