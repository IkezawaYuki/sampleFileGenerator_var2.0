import tkinter.messagebox
from operator import itemgetter


def xstr(s):
    return "" if s is None else str(s)


def reading_file_koumoku(sheet):
    """
    項目情報を読み取る。ここで読み込んだ情報がサンプルファイルのヘッダーやデータの型などに直接影響する。
    :param sheet:　変換定義書の「項目情報」のシート
    :return:
    """
    row_index = 0

    # 入力元テキストファイル項目情報がどこから始まるのかを確認
    while True:
        row_info = sheet.row(row_index)
        info_column = xstr(row_info[1].value)
        if "入力元テキストファイル" in info_column or "入力元ファイル" in info_column:
            row_index += 2
            break
        row_index += 1
        if row_index > 100:
            tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                         "一度環境にアップロードしたもののみサンプルデータを作成できます。")
            raise IOError

    if "可変" in info_column:
        print("可変長")
        files_list, row_index = read_koumku_ver_kahen(row_index, sheet)
    else:
        print("固定長")
        files_list, row_index = read_koumoku_ver_kotei(row_index, sheet)
    join_info = read_join_info(row_index, sheet)
    return files_list, join_info


def read_koumoku_ver_kotei(index, sheet):
    """
    固定長ファイルの情報を読み込むメソッド

    """
    files_list = []  # ファイル全ての情報のリスト
    file_info = []  # inファイル単位の情報
    row_index = index

    # ここで項目情報を１行１行取得している。
    # １行１行がタプル、それらが入力元名称で配列に分けられている、それらは全体で一つの配列にはいっている。
    while True:
        row_info = sheet.row(row_index)
        file_name = xstr(row_info[2].value)
        item = xstr(row_info[3].value)
        start_byte = row_info[4].value
        end_byte = row_info[5].value
        how_to_pack = xstr(row_info[6].value)
        filling_character = xstr(row_info[7].value)
        date_format = xstr(row_info[9].value)

        if file_name == "" and item == "":
            files_list.append(file_info[:])
            break

        if file_name != "" and len(file_info) > 0:
            files_list.append(file_info[:])
            file_info.clear()

        file_info_temp = (file_name, item, start_byte, end_byte, how_to_pack,
                          filling_character, date_format)
        file_info.append(file_info_temp)

        row_index += 1
    return files_list, row_index


def read_koumku_ver_kahen(index, sheet):
    """
    可変長のファイルの情報を読み込むメソッド

    """
    files_list = []  # ファイル全ての情報のリスト
    file_info = []  # inファイル単位の情報
    row_index = index

    # ここで項目情報を１行１行取得している。
    # １行１行がタプル、それらが入力元名称で配列に分けられている、それらは全体で一つの配列にはいっている。
    while True:
        row_info = sheet.row(row_index)
        file_name = xstr(row_info[2].value)
        item = xstr(row_info[3].value)
        column_index = row_info[4].value
        close_character = xstr(row_info[5].value)
        date_format = xstr(row_info[6].value)

        if file_name == "" and item == "" and column_index == "":
            files_list.append(file_info[:])
            break

        if file_name != "" and len(file_info) > 0:
            files_list.append(file_info[:])
            file_info.clear()

        file_info_temp = (file_name, item, column_index, close_character, date_format)
        file_info.append(file_info_temp)

        row_index += 1
    return files_list, row_index


def read_join_info(index, sheet):
    """
    結合に使われているカラムの情報を取得するメソッド
    :param index: 入力元のファイル項目情報を読み込んだあとの行数
    :param sheet: 変換定義書の項目情報のシート
    :return:　結合情報のリスト
    """
    row_index = index + 3
    row_info = sheet.row(row_index)
    if "入力" in xstr(row_info[2].value):
        row_index += 1
    else:
        return None
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
    """
    項目情報から読み込んだ入力元ファイルの項目情報をカラム順にソートするメソッド
    :param file_list: 入力元テキスト項目情報、１行１行の情報
    :return: カラム位置順にソートされたもの。
    """
    files = file_list[:]
    sorted_result = []
    for temp in files:
        sort_list = sorted(temp, key=itemgetter(2))
        sorted_result.append(sort_list[:])
    print(sorted_result)
    return sorted_result



def reading_file_kihon(sheet):
    """
    基本情報を読み込むメソッド。この情報がファイルの名称、文字コードなどに直接影響する。
    :param sheet: 変換定義書の基本情報
    :return:
    """
    row_index = 1
    file_kihon_list = []

    while True:
        row_info = sheet.row(row_index)
        info_column = xstr(row_info[1].value)
        if "入力元ファイル" in info_column or "入力元テキストファイル" in info_column:
            row_index += 2
            break
        row_index += 1
        if row_index > 100:
            tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                         "一度環境にアップロードしたもののみサンプルデータを作成できます。")
            raise IOError

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
                tkinter.messagebox.showinfo('inspect -sample file generator ver3.0-',
                                            "一度環境にアップロードしたもののみサンプルデータを作成できます。")
                raise IOError
            break
        temp_file_info = (file_name, encode, format_kind, new_line_code, delimiter, header)
        file_kihon_list.append(temp_file_info)
        row_index += 1
    return file_kihon_list
