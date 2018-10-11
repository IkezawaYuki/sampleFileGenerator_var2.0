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
    temp_rows = []
    while True:
        try:
            row_info = sheet.row(row_index)
            henkan_name = xstr(row_info[2].value)
            lane = row_info[3].value
            order = row_info[4].value
            details = (xstr(row_info[5].value), xstr(row_info[6].value), xstr(row_info[7].value),
                       xstr(row_info[8].value), xstr(row_info[9].value), xstr(row_info[10].value),
                       xstr(row_info[11].value), xstr(row_info[12].value), xstr(row_info[13].value),
                       xstr(row_info[14].value))

            key = create_key(lane, order)

            if henkan_name == "" and lane == "" and order == "":
                break

            if len(converte_rows) != 0 and lane == "1":
                converte_rows.append(temp_rows)

            henkan_row = (key, details)
            temp_rows.append(henkan_row)

            row_index += 1
        except IndexError:
            converte_rows.append(temp_rows)
            break
    print(converte_rows)
    return converte_rows


def inspection(convete_rows):
    target = [0 for i in range(len(convete_rows[0]))]
    print(target)

    for i, row in enumerate(convete_rows[0]):


        print(row)
        print(i)
        if row is not None:
            target[i] = 1

    for j in target:
        if j == 0:
            print(j)


def execute_coverage_test(sheet):
    """　変換定義の詳細情報がすべて通る可能性があるかどうか """
    print("go throws")
    converte_rows = read(sheet)
    if inspection(converte_rows):
        return True
    else:
        return False
