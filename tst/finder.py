import os
import platform
import glob

scan_dir_path = input("Введите директорию для сканирования > ")
try:
    list_scan_file = list(os.listdir(scan_dir_path))
    print(list_scan_file)
except:
    print("Такая директория не найдена")
    exit(-1)

log_dir = os.getcwd()
work_dir = os.getcwd()
file_extension = re.compile(r'.\.txt$')
list_copied_file = []

if platform.system() == 'Windows':
    result_file = open(work_dir + "\\result.txt", "a", encoding="utf-8")
else:
    result_file = open(work_dir + "/result.txt", "a", encoding="utf-8")

list_scan_file = list(filter(lambda x: 'txt' in x, list_scan_file))
for file_name in list_scan_file:
    check_file_extension = re.match(file_extension, file_name)
    if platform.system() == 'Windows':
        scanned_file = open(scan_dir_path + "\\" + file_name, "r+", encoding='utf-8')
    else:
        scanned_file = open(scan_dir_path + "/" + file_name, "r+", encoding='utf-8')
    result_file.write("\n" + scanned_file.read() + "\n*****\n")
    scanned_file.close()
    list_copied_file.append(file_name)
result_file.close()

if str(platform.system()) == 'Windows':
    log_file = open(log_dir + "\\result.log", "a")
else:
    log_file = open(log_dir + "/result.log", "a")
log_file.write(
    str(scan_dir_path) + "\n" + str(len(list_copied_file)) + "\n" + str(list_copied_file) + "\n===============\n")
log_file.close()
