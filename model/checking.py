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
            tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
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

            if len(row_info) == 14:
                details = [xstr(row_info[5].value), xstr(row_info[6].value), xstr(row_info[7].value),
                           xstr(row_info[8].value), xstr(row_info[9].value), xstr(row_info[10].value),
                           xstr(row_info[11].value), xstr(row_info[12].value), xstr(row_info[13].value),
                           None]
            else:
                details = [xstr(row_info[5].value), xstr(row_info[6].value), xstr(row_info[7].value),
                       xstr(row_info[8].value), xstr(row_info[9].value), xstr(row_info[10].value),
                       xstr(row_info[11].value), xstr(row_info[12].value), xstr(row_info[13].value),
                       xstr(row_info[14].value)]


            # 読み込む行がなくなった時
            if lane == "" and order == "":
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
    return converte_rows


def inspect_main(key, group, rooting):
    """
    変換詳細情報のチェックのメインルーチン。各行に対して、通った行にはTrue、通らなかった行はFalseとなる。
    :param key: レーン、順序から作った３桁のキー
    :param group: 変換詳細の情報を、変換名称ごとに分けたもの。
    :param rooting: 処理の軌跡
    :return:
    """
    roots = rooting.copy()
    roots.append(key)
    print(roots)
    try:
        temp = group[key]
        for num, cell in enumerate(temp):
            if cell is None:
                continue
            elif num == 10:
                if temp[10] is False:
                    temp[10] = True
                togo = increment_key(key)
                if togo in group:
                    print("let's go", str(togo))
                    inspect_main(togo, group, roots)
                break
            elif ">>" in cell:
                togo = adjust_togo(cell)
                inspect_main(togo, group, roots)
            elif ">" in cell:
                togo = adjust_togo(cell)
                if togo in roots:
                    continue
                else:
                    tkinter.messagebox.showerror('Sinspect -sample file generator ver3.0-',
                                                 "変換詳細情報に通っていない結果を参照している箇所があります。以下の変換詳細情報を見直してください \n" + str(temp))
                    exit(0)
    except KeyError:
        error_row = rooting[-1]
        tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                     "変換詳細情報に存在しない箇所を参照している箇所があります。以下の変換詳細情報を見直してください \n" + str(group[error_row]))
        exit(0)
    except RecursionError:
        error_row = rooting[-1]
        tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                     "変換詳細情報に無限ループが存在しています。以下の変換詳細情報を見直してください。\n" + str(group[error_row]))
        exit(0)


def increment_key(key):
    temp_base = str(key)
    temp = temp_base[-2:]
    if temp == "09":
        key = temp_base[:-1] + "10"
        print(key)
        return int(key)
    else:
        return key + 1


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
    for i in converte_rows:
        print(i)

    print("--check--")
    if len(converte_rows[0]) == 0:
        return True

    for group in converte_rows:
        rooting = []
        inspect_main(101, group, rooting)

    print('check finish!')

    for group in converte_rows:
        results = group.values()
        for result in results:
            if result[10] is False:
                print(result)
                tkinter.messagebox.showerror(
                    'inspect -sample file generator ver3.0-',
                    "変換詳細情報に通っていない処理が存在しています。以下の変換詳細情報を見直してください。\n" + group)
                return False
            else:
                continue
    return True

