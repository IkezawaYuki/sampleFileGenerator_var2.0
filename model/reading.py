import tkinter.messagebox
from operator import itemgetter

def xstr(s):
    return "" if s is None else str(s)


def reading_file_koumoku(sheet):
    files_list = []   #ファイル全ての情報のリスト
    file_info = []    #inファイル単位の情報

    row_index = 6
    while True:
        row_info = sheet.row(row_index)
        file_name = xstr(row_info[2].value)
        item = xstr(row_info[3].value)
        column_index = row_info[4].value
        close_character = xstr(row_info[5].value)
        date_format = xstr(row_info[6].value)

        if file_name == "" and item == "" and column_index == "":
            if file_name == "" and row_index == 6:
                tkinter.messagebox.showinfo('Sample file generator ver2.0',
                                            "一度環境にアップロードしたもののみサンプルデータを作成できます。")
                raise IOError
            files_list.append(file_info[:])
            break

        if file_name != "" and row_index != 6:
            files_list.append(file_info[:])
            file_info.clear()

        file_info_temp = (file_name, item, column_index, close_character, date_format)
        file_info.append(file_info_temp)

        row_index += 1

    join_info = read_join_info(row_index, sheet)
    return files_list, join_info


def read_join_info(index, sheet):
    row_index = index + 3
    row_info = sheet.row(row_index)
    if "入力" in xstr(row_info[2].value):
        row_index += 1
    else:
        tkinter.messagebox.showinfo('Sample file generator ver2.0',
                                    "一度環境にアップロードしたもののみサンプルデータを作成できます。")
        raise IOError
    join_info_list = []
    while True:

        row_info = sheet.row(row_index)

        file_name = xstr(row_info[2].value)
        item = xstr(row_info[3].value)

        if file_name == "":
            break

        temp = (file_name, item)
        join_info_list.append(temp)

        file_name_join = xstr(row_info[5])
        item_join = xstr(row_info[6])
        temp = (file_name_join, item_join)
        join_info_list.append(temp)

        row_index += 1
    return join_info_list


def sorted_list(file_list):
    files = file_list[:]
    sorted_result = []
    for temp in files:
        sort_list = sorted(temp, key=itemgetter(2))
        sorted_result.append(sort_list[:])
    print(sorted_result)
    return sorted_result


def reading_file_kihon(sheet):
    row_index = 26
    file_kihon_list = []
    while True:
        row_info = sheet.row(row_index)
        file_name = xstr(row_info[2].value)
        encode = xstr(row_info[5].value)
        format_kind = xstr(row_info[6].value)
        new_line_code = xstr(row_info[7].value)
        delimiter = xstr(row_info[8].value)
        header = xstr(row_info[13].value)

        if file_name == "":
            if file_name == "" and row_index == 26:
                tkinter.messagebox.showinfo('Sample file generator ver2.0',
                                            "一度環境にアップロードしたもののみサンプルデータを作成できます。")
                raise IOError
            break
        temp_file_info = (file_name, encode, format_kind, new_line_code, delimiter, header)
        file_kihon_list.append(temp_file_info)
        row_index += 1
    return file_kihon_list
