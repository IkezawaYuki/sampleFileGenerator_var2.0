import csv
from _datetime import datetime
import xlrd
import os
import tkinter.filedialog
import tkinter.messagebox

import model.reading as read
import model.writing as write
import model.checking as check


def main():
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("", "*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    # file = tkinter.filedialog.askopenfilenames(filetypes=fTyp, initialdir=iDir)
    # file = "/Users/ikezaway/PycharmProjects/sampleFileGenerator/basic_join.xlsx"
    file = "/Users/ikezaway/Downloads/test_data/IF52700099.xlsx"


    if file == "":
        exit(0)

    if type(file) is tuple:
        for f in file:
            if "xls" not in f:
                c = tkinter.messagebox.showerror('Sample file generator ver2.0',
                                                 '以下のファイルは変換定義書ではありません。\n' + f)
                continue
            print(f + " is executing...")
            execute(f)
    else:
        if "xls" not in file:
             c = tkinter.messagebox.showerror('Sample file generator ver2.0',
                                              '変換定義書ではありません。')
             exit(0)
        execute(file)


    tkinter.messagebox.showinfo('Sample file generator ver2.0',
                                              '処理が正常終了しました。')
    exit(0)


def execute(file):
    wb = xlrd.open_workbook(file)
    basic_info_list = []
    join_info = []
    sort_list = []

    for page in range(wb.nsheets):
        sheet = wb.sheet_by_index(page)

        if sheet.name == "基本情報":
            basic_info_list = read.reading_file_kihon(sheet)

        if sheet.name == "項目情報":
            in_files, join_info = read.reading_file_koumoku(sheet)
            sort_list = read.sorted_list(in_files)

        if sheet.name == "変換詳細情報":
            if check.execute_coverage_test(sheet) is False:
                c = tkinter.messagebox.showerror('Sample file generator ver2.0',
                                                 '変換詳細情報を確認してください。')
    write.generate_file(basic_info_list, sort_list, join_info, file)
    return True


if __name__ == "__main__":
    main()
