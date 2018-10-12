import tkinter.messagebox
import math


def xstr(s):
    return "" if s is None else str(s)


class Rows:
    def __init__(self, num, one, two, three, four, five, six):
        self.number = num
        self.one = one
        self.two = two
        self.three = three
        self.four = four
        self.five = five
        self.six = six


def create_key(lane, order):
    lane = math.floor(lane)
    order = math.floor(order)
    key = str(lane) + "0" + str(order)
    key = int(key)
    return key


def read(sheet):
    row_index = 1

    while True:
        row_info = sheet.row(row_index)
        info_column = xstr(row_info[1].value)
        if "変換詳細" in info_column:
            row_index += 2
            break
        row_index += 1
        if row_index > 100:
            tkinter.messagebox.showerror('Sample file generator ver2.0',
                                         "一度環境にアップロードしたもののみサンプルデータを作成できます。")
            raise IOError

    converte_rows = []
    temp_rows = {}
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



            if henkan_name == "" and lane == "" and order == "":
                break

            print(lane)
            print(order)
            print(type(lane))
            key = create_key(lane, order)

            if len(converte_rows) != 0 and lane == "1":
                converte_rows.append(temp_rows)

            # konomamadeha
            if key in temp_rows:
                converte_rows.append(temp_rows)

            temp_rows[key] = details

            row_index += 1
        except IndexError:
            converte_rows.append(temp_rows)
            break
    print(converte_rows)
    return converte_rows


def inspect_main(key, group):

    try:
        temp = group[key]
        for num, cell in enumerate(temp):
            if num == 0:
                temp[0] = True
            elif ">>" in cell:
                togo = cell[-2:-1]
                togo = int(togo + "00")
                key += togo
                inspect_main(key, group)
            elif ">" in cell:
                togo = cell[2] + "0" + cell[4]
                togo = int(togo)
                inspect_main(togo, group)
    except ValueError:
        return



def inspection(convete_rows):

    pass
    #　辞書型にして再帰呼び出しするメソッドに渡す




def execute_coverage_test(sheet):
    """　変換定義の詳細情報がすべて通る可能性があるかどうか """
    converte_rows = read(sheet)

    for group in converte_rows:
        inspect_main(101, group)

    print(converte_rows)

    for group in converte_rows:
        if group[0] is False:
            raise ValueError

