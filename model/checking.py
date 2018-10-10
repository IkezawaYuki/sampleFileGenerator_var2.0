import tkinter.messagebox

def xstr(s):
    return "" if s is None else str(s)


def read(sheet):
    row_index = 0

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
        row_info = sheet.row(row_index)
        henkan_name = xstr(row_info[2].value)
        lane = xstr(row_info[3].value)
        order = row_info[4].value
        details = (xstr(row_info[5].value), xstr(row_info[6].value), xstr(row_info[7].value),
                   xstr(row_info[8].value), xstr(row_info[9].value), xstr(row_info[10].value),
                   xstr(row_info[11].value), xstr(row_info[12].value), xstr(row_info[13].value),
                   xstr(row_info[14].value))

        if henkan_name == "" and lane == "" and order == "":
            break

        if len(converte_rows) != 0 and lane == "1":
            converte_rows.append(temp_rows)

        henkan_row = (lane, order, details)
        temp_rows.append(henkan_row)

        row_index += 1

    return converte_rows


def inspection(convete_rows):
    pass




def execute_coverage_test(sheet):
    """　変換定義の詳細情報がすべて通る可能性があるかどうか """

    converte_rows = read(sheet)
    if inspection(converte_rows):
        return True
    else:
        return False
