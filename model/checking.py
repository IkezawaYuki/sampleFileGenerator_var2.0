import tkinter.messagebox
import math


def xstr(s):
    return "" if s is None else str(s)


def create_key(lane, order):
    """
    レーン、順序から作った３桁のキーを作る
    :param lane: 変換詳細の「レーン」の数字
    :param order: 変換詳細の「順序」の数字
    :return:　３桁のint型のkey
    """
    lane = math.floor(lane)
    order = math.floor(order)
    key = str(lane) + "0" + str(order)
    key = int(key)
    return key


def read_convert_info(sheet):
    """
    :param sheet: 変換定義の「変換詳細情報」のシート

    """
    row_index = 1

    # 変換詳細がどこから始まるのかを探す
    while True:
        row_info = sheet.row(row_index)
        info_column = xstr(row_info[1].value)
        if "変換詳細" in info_column:
            row_index += 2
            break
        row_index += 1
        if row_index > 300:
            tkinter.messagebox.showerror('Sample file generator ver2.0',
                                         "一度環境にアップロードしたもののみサンプルデータを作成できます。")
            raise IOError

    converte_rows = []
    temp_rows = {}

    # 変換詳細を読み込む際に、変換名称ごとにレーン、順序をキーに辞書にし、全体をconverte_rowsに入れている。
    while True:
        try:
            row_info = sheet.row(row_index)
            henkan_name = xstr(row_info[2].value)
            lane = row_info[3].value
            order = row_info[4].value
            details = [xstr(row_info[5].value), xstr(row_info[6].value), xstr(row_info[7].value),
                       xstr(row_info[8].value), xstr(row_info[9].value), xstr(row_info[10].value),
                       xstr(row_info[11].value), xstr(row_info[12].value), xstr(row_info[13].value),
                       xstr(row_info[14].value)]

            # 読み込む行がなくなった時
            if henkan_name == "" and lane == "" and order == "":
                break

            if henkan_name != "" and len(temp_rows) != 0:
                converte_rows.append(temp_rows)
                temp_rows = {}

            key = create_key(lane, order)

            details.append(False)
            temp_rows[key] = details

            row_index += 1
        # 読み込む行数がなくなった場合、その境界値でエラーが頻発するため、exeptで対処している。
        except IndexError:
            converte_rows.append(temp_rows)
            break
    print(converte_rows)
    for i in converte_rows:
        print(i)
    print("--上がデータ構造--")
    return converte_rows


def inspect_main(key, group):
    """
    変換詳細情報のチェックのメインルーチン。各行に対して、通った行にはTrue、通らなかった行はFalseとなる。
    :param key: レーン、順序から作った３桁のキー
    :param group: 変換詳細の情報を、変換名称ごとに分けたもの。
    :return:
    """

    try:
        temp = group[key]
        print(temp)
        for num, cell in enumerate(temp):
            if num == 10:
                if temp[10] is False:
                    temp[10] = True
                else:
                    return
                togo = key + 1
                if togo in group:
                    print("let's go")
                    inspect_main(togo, group)
                break
            elif ">>" in cell:
                key = adjust_togo(cell)
                inspect_main(key, group)
            elif ">" in cell:
                n = key
                key = adjust_togo(cell)
                if group[key][10] is True:
                    key = n
                    continue
                else:
                    tkinter.messagebox.showerror('Sample file generator ver2.0',
                                                 "変換詳細情報に不備が存在しています。")
    except KeyError:
        tkinter.messagebox.showerror('Sample file generator ver2.0',
                                     "変換詳細情報に不備が存在しています。")
    except RecursionError:
        tkinter.messagebox.showerror('Sample file generator ver2.0',
                                     "変換詳細情報に無限ループが存在している可能性があります。")



def adjust_togo(cell):
    """
    >1-1 や >>2などの値をkeyの形（101などの３桁）に修正するメソッド
    :param cell: 「>」「>>」が存在するセル
    :return: ３桁の数、key
    """
    if ">>" in cell:
        n = cell.rfind(">")
        togo = cell[n + 1:]
        togo = int(togo + "01")
        return togo
    elif ">" in cell:
        print(cell)
        n = cell.rfind(">")
        togo = cell[n + 1:]
        togo = int(togo.replace("-", "0"))
        return togo


def execute_coverage_test(sheet):
    """
    変換定義の詳細情報がすべて通る可能性があるかどうかのチェックを行うメソッド
    :param sheet: 変換定義書の「変換詳細情報」のシート
    :return: 通らない行が存在する場合、この時点でエラーメッセージ出力
    """
    converte_rows = read_convert_info(sheet)

    for group in converte_rows:
        inspect_main(101, group)

    print(converte_rows)

    for group in converte_rows:
        results = group.values()
        for result in results:
            if result[10] is False:
                print("False")
                return False
            else:
                print("True good job")
    return True

