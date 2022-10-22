import glob
import os.path
from os.path import join
import sys

file_res = {}
dirr = input()
try:
    assert os.path.exists(dirr)
    print(1)
except:
    print('дирректория не найдена')
    sys.exit(0)
files = [file for file in glob.glob('test1.txt', root_dir=dirr)]
file_count = len(files)
for file in files:
    with open(join('', file), encoding='utf-8') as f:
        file_res.update({file: f.read()})

with open('res.log', 'w', encoding='utf-8') as log:
    res = f"""
    dir path {dirr}
    files_count {file_count}
    files are {files}
    
    """
    log.write(res)
with open('result.txt', 'w', encoding='utf-8') as res:
    for k, v in file_res.items():
        res.write(f'{k}\n{v}\n')
