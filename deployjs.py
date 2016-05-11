import subprocess
from os import path
import os

basedir = path.abspath(path.dirname(__file__))
static_index_path = path.join(basedir, 'static/index.html')
scripts_index_path = path.join(basedir, 'static/scripts')
styles_index_path = path.join(basedir, 'static/styles')


def build_with_gulp():
    output = subprocess.check_output(
        'cd webapp && gulp deploy && cd ..',
        shell=True,
    )
    print output


def js_processing(all_lines):
    for each_line in all_lines:
        if "scripts/" in each_line:
            newLine = each_line[30:].split('"></script><script src="scripts/')
            first = newLine[0]
            second = newLine[1].split("></script></body></html>")[0][0:-1]
            return first, second


def css_processing(all_lines):
    for each_line in all_lines:
        if "css" in each_line:
            a = each_line.split('<link rel="stylesheet" href="styles/')
            css_1 = a[1].split('">')[0]
            css_2 = a[2].split('">')[0]
            return css_1, css_2


def read_new_index_file():
    with open(static_index_path, 'r') as f:
        all_lines = f.readlines()
    scripts = js_processing(all_lines)
    css_files = css_processing(all_lines)
    delete_files(scripts, scripts_index_path)
    delete_files(css_files, styles_index_path)


def delete_files(files_to_keep, dir_path):
    for subdir, dirs, files in os.walk(dir_path):
        # for each file
        for file in files:
            filepath = subdir + os.sep + file

            # for each file to keep
            found_one_match = False
            for file_to_keep in files_to_keep:
                if file_to_keep in filepath:
                    found_one_match = True
            if not found_one_match:
                os.remove(filepath)


def kick_off():
    build_with_gulp()
    read_new_index_file()


if __name__ == "__main__":
    kick_off()
