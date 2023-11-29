Computes SHA-1 checksum for all the files in the specified directory or for the list of all files specified in a file and writes to a `checksum.txt` file.

**Usage:**

`pride_checksum --out_path /path/to/save/computed_checksum/ --files_dir /dir_path/where/files/are/located/`

OR

`pride_checksum --out_path /path/to/save/computed_checksum/ --files_list_path /path/to/file/containing/list_of_files.txt`

Sample `list_of_files.txt`:
```
/path/to/some/file1.xml
/path/to/some/file2.xml
/some/other/path/file3.tsv
```
Please make sure the list of files:
* Doesn't contain any duplicate file names.
* Doesn't contain any directories (only files are allowed)
* Doesn't contain any hidden files.


***NOTE:***
* **File names can't have any spaces or any special chars other than underscore(_) and hyphen (-)**

* The name of the output file is always `checksum.txt` and if a file with same name already exists in the specified out_path, it will be overwritten. 