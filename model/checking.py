import tkinter.messagebox
import math
import sys

import generator_config as l


def xstr(s):
    return "" if s is None else str(s)


def create_key(lane, order):
    """
    レーン、順序からキーを作る
    レーン1、順序4の場合、104となる。レーン2、順序10の場合、210ではなく、2010になる点に注意。
    :param lane: 変換詳細の「レーン」の数字
    :param order: 変換詳細の「順序」の数字
    :return: キー
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
    group_name = []

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
                           xstr(None)]
            else:
                details = [xstr(row_info[5].value), xstr(row_info[6].value), xstr(row_info[7].value),
                       xstr(row_info[8].value), xstr(row_info[9].value), xstr(row_info[10].value),
                       xstr(row_info[11].value), xstr(row_info[12].value), xstr(row_info[13].value),
                       xstr(row_info[14].value)]

            if henkan_name != "":
                group_name.append(henkan_name)

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
    return converte_rows, group_name


def reference_row(key, group, g_name):
    """
    このメソッドで、参照先の行に問題がないかどうかをチェックする。
    変換定義の仕様上、ある行が>2-3としていて、そのレーン2、順序3の行に>>4、などとある場合、正しく動作しない。
    >?-? の先に　>>?　が存在しないかどうかをチェックする必要がある。
    """
    temp = group[key]
    for num, cell in enumerate(temp):
        if num == 10:
            return False
        if ">>" in cell:
            l.logger.info(g_name + " " + str(key) + " is dangerous logic.")
            tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                         "以下の行を参照しようとする際、問題が起きる可能性があります。\nロジックを修正してください。\n\n変換名称：" + g_name + "\n\n" + str(temp))
            sys.exit(0)


def inspect_main(key, group, rooting, g_name):
    """
    変換詳細情報のチェックのメインルーチン。各行に対して、通った行にはTrue、通らなかった行はFalseとなる。
    ロジックは「深さ優先探索」を採用。
    :param key: レーン、順序から作ったキー
    :param group: 変換詳細の情報を、変換名称ごとに分けたもの。
    :param rooting: 処理の軌跡
    :return:
    """
    # todo 深さ優先探索⇒幅優先探索に要変更。コードが汚れてきたので、リファクタリングも。
    roots = rooting.copy()
    roots.append(key)
    try:
        temp = group[key]
        for num, cell in enumerate(temp):
            if num == 10:
                if temp[10] is False:
                    temp[10] = True
                togo = increment_key(key)
                if togo in group:
                    inspect_main(togo, group, roots, g_name)
                # todo ここにelifで「>>」があったかどうかを確認する必要がある。
                # あった場合はその処理に。なかった場合はbreakするスクリプトが必要。

                break
            elif ">>" in cell:
                # todo おそらくflagが必要。もしくは変数として再帰呼び出しの際に、参照できるようにしなければならない。
                togo = adjust_togo(cell)
                inspect_main(togo, group, roots, g_name)
            elif ">" in cell:
                togo = adjust_togo(cell)
                if togo in roots:
                    if reference_row(togo, group, g_name):
                        continue
                else:
                    l.logger.info(g_name + " " + str(key) + ". There is a possibility of NullPointerException")
                    error_row = str(key)
                    error_row = error_row.replace("0", " 順序：")
                    tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                                 "変換詳細情報に \"通っていない行を参照している箇所\" があります。\n\n変換名称：" + g_name + "\n\n レーン：" + str(error_row))
                    sys.exit(0)
    except KeyError:
        error_row = str(key)
        error_row = error_row.replace("0", " 順序：")
        l.logger.info(g_name + " " + str(key) + ". There is a possibility of NullPointerException")
        tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                     "変換詳細情報に \"存在しない箇所を参照している行\" があります。\n\n変換名称：" + g_name+ "\n\n レーン：" + str(error_row))
        sys.exit(0)
    except RecursionError:
        l.logger.info(g_name + " " + str(key) + ". There is a infinite loop")
        tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                     "変換詳細情報に \"無限ループ\" が存在しています。\n\n変換名称：" + g_name)
        sys.exit(0)


def increment_key(key):
    temp_base = str(key)
    temp = temp_base[-2:]
    if temp == "09":
        key = temp_base[:-1] + "10"
        l.logger.info(key)
        return int(key)
    else:
        return key + 1


def adjust_togo(cell):
    """
    >1-1 や >>2などの値をkeyの形（101などの３桁）に修正するメソッド
    注意が必要なのは109の次は110ではなく1010になる点
    :param cell: 「>」「>>」が存在するセル　例）>3-1
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
    :return: 通らない行が存在する場合、この時点でエラーメッセージ出力、問題なければTrueを返す。
    """
    converte_rows, group_name = read_convert_info(sheet)

    l.logger.info("check is start.")
    if len(converte_rows) == 0:
        l.logger.info("converte_rows is length 0")
        return True

    if len(converte_rows[0]) == 0:
        l.logger.info("converte_rows[0] is length 0.")
        return True

    for num, group in enumerate(converte_rows):
        g_name = group_name[num]
        rooting = []
        inspect_main(101, group, rooting, g_name)

    for num, group in enumerate(converte_rows):
        results = group.values()
        for result in results:
            if result[10] is False:
                tkinter.messagebox.showerror(
                    'inspect -sample file generator ver3.0-',
                    "変換詳細情報に \"通っていない行\" が存在しています。\n以下の変換詳細情報を見直してください。\n\n変換名称：" + group_name[num] + "\n\n" + str(result))

                sys.exit(0)
            else:
                continue
    l.logger.info("There is no error caused by logic in data hub.")
    return True

