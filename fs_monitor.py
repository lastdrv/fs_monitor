import os
import sys

OUT_FILE = 'fs_monitor.out'
EXCLUDES = ['automysqlbackup']  # список строк исключений, можно добавлять


def diff_files(old_file: str, new_file: str):
    new_dict = file_to_dict(new_file)
    old_dict = file_to_dict(old_file)
    diff_dict = {}

    for key in new_dict.keys():
        old_value = old_dict.get(key, 0)
        if new_dict[key] - old_value > 0:
            diff_dict[key] = new_dict[key] - old_value, new_dict[key]

    diff_dict = {k: (str(v[0]) + 'M', str(v[1]) + 'M') for k, v in
                 sorted(diff_dict.items(), key=lambda item: item[1], reverse=True)}

    with open(OUT_FILE, 'w') as out_file:
        for key, val in diff_dict.items():
            val = val[0] + ', ' + (' - ' if val[0] == val[1] else val[1])
            out_file.write(f'{val}: {key}\n')


def file_to_dict(file: str) -> dict:
    result_dict = {}
    with open(file, 'r') as strings:
        for line in strings:
            set_of_exclude = {line.find(exclude) for exclude in EXCLUDES}
            if len(set_of_exclude) != 1 or set_of_exclude.pop() != -1:
                continue
            (key, val) = line.split()
            result_dict[val] = int(key[:-1])
    return result_dict


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Параметры запуска fs_monitor <старый файл> <свежий файл>')
        print('оба файла должны находиться в каталоге скрипта')
        exit(1)
    diff_files(os.getcwd() + '/' + sys.argv[1], os.getcwd() + '/' + sys.argv[2])
