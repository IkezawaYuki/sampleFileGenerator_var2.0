import tkinter.messagebox
import math
import sys
import pprint

import generator_config as l


def xstr(s):
    return "" if s is None else str(s)


class ConversionDetailedGroup:
    def __init__(self, conversion_row, name):
        self.conversion_rows = dict(conversion_row)
        self.check_result = False
        self.error_msg = []
        self.name = name
        self.lane = []
        self.statement = True

        before = 100
        temp_row = []
        for key in self.conversion_rows.keys():
            temp1 = str(before)[:2]
            temp2 = str(key)[:2]
            before = key
            if temp1 == temp2:
                temp_row.append(key)
            else:
                self.lane.append(temp_row[:])
                temp_row.clear()
                temp_row.append(key)
        self.lane.append(temp_row)

    def through_all_check(self):
        if len(self.error_msg) > 0:
            print("There are error!!")
            print(self.error_msg)

        for key, rows in self.conversion_rows.items():
            if rows[-1] is False:
                print(key)
                self.error_msg.append("通っていない行があります。\n"
                                      "変換名称 : {}\nレーン {} 順序 {}".format(self.name, str(key)[0], str(key)[2]))

    def show_error_msg(self):
        if len(self.error_msg) == 0:
            return
        for msg in self.error_msg:
            yes = tkinter.messagebox.askyesno('inspect -sample file generator ver3.0-', msg + "\n\n処理を中断しますか？")
            if yes:
                sys.exit(0)

    def __bool__(self):
        return self.statement


class Inspect:
    def __init__(self):
        self.key = 101
        self.jump_stack = []
        self.rooting = []

    def cell_scan(self, cell):
        if ">>" in cell:
            jump = adjust_togo(cell)
            self.jump_stack.append(jump)
        elif ">" in cell:
            root = adjust_togo(cell)
            if root not in self.rooting:
                return False
            #todo 無限ループの可能性を検出するロジックの追加。

        return True

    def row_scan(self, c_group, c_row, key):
        for num, cell in enumerate(c_row):
            if num == 10:
                c_row[10] = True
                continue
            result = self.cell_scan(cell)
            if result is False:
                c_group.statement = False
                c_group.error_msg.append("NullPointerExceptionが発生しています。\n"
                                         "変換名称 : {}\nレーン {} 順序 {}".format(c_group.name, str(key)[0], str(key)[2]))
        self.rooting.append(key)

    def lane_scan(self, c_group, lane):
        i = 1
        for key in lane:
            if str(i) != str(key)[-1]:
                c_group.error_msg.append("処理を飛ばす先が存在しません。\n"
                                         "変換名称 : {}\nレーン {} 順序 {}".format(c_group.name, str(key)[0], str(key)[2]))
            target_rows = c_group.conversion_rows[key]
            self.row_scan(c_group, target_rows, key)
            i += 1

    def inspect_main(self, group):
        temp = group.lane.pop(0)
        self.lane_scan(group, temp)
        while len(self.jump_stack) > 0:
            jump_key = self.jump_stack.pop(0)
            i = 0
            for lists in group.lane:
                if jump_key in lists:
                    self.lane_scan(group, lists)
                    group.lane.pop(i)
                    break
                i += 1
            else:
                group.error_msg.append("処理を飛ばす先が存在しません。\n"
                                       "変換名称 : {}\n飛ばす先のレーン : {}".format(group.name, str(jump_key)[0]))

    def adjust_togo(cell):
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

    def __str__(self):
        return str(self.group_name)




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
            yes = tkinter.messagebox.askyesno('inspect -sample file generator ver3.0-',
                                         "以下の行を参照しようとする際、問題が起きる可能性があります。\n処理を中断しますか？\n\n変換名称：" + g_name + "\n\n" + str(temp))
            if yes:
                sys.exit(0)



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
        pprint.pprint(group)
        c_row = ConversionDetailedGroup(group, g_name)
        inspect = Inspect()
        inspect.inspect_main(c_row)
        c_row.through_all_check()
        c_row.show_error_msg()

    l.logger.info("There is no error caused by logic in data hub.")
    return True

