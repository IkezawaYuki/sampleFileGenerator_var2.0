import csv
from _datetime import datetime
import xlrd
import os
import tkinter.filedialog
import tkinter.messagebox

import model.reading as read
import model.writing as write


def main():
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("", ".xlsx")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    # file = tkinter.filedialog.askopenfilenames(filetypes=fTyp, initialdir=iDir)
    file = "/Users/ikezaway/PycharmProjects/sampleFileGenerator/IF21000099.xlsx"
    #file = ("/Users/ikezaway/PycharmProjects/sampleFileGenerator/IF00100051.xlsx",
    # "/Users/ikezaway/PycharmProjects/sampleFileGenerator/IF21000099.xlsx")

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

    exit(0)


def execute(file):
    wb = xlrd.open_workbook(file)
    basic_info_list = []
    join_info = []
    sort_list = []

    for page in range(wb.nsheets):
        sheet = wb.sheet_by_index(page)
        if sheet.name != "項目情報" and sheet.name != "基本情報":
            continue

        if sheet.name == "基本情報":
            basic_info_list = read.reading_file_kihon(sheet)

        if sheet.name == "項目情報":
            in_files, join_info = read.reading_file_koumoku(sheet)
            sort_list = read.sorted_list(in_files)

    write.generate_file(basic_info_list, sort_list, join_info, file)
    return True

if __name__ == "__main__":
    main()
