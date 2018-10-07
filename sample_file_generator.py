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
    fTyp = [("", "*")]
    iDir = os.path.abspath(os.path.dirname(__file__))

    # file = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
    file = "/Users/ikezaway/PycharmProjects/sampleFileGenerator/IF00100051.xlsx"


    if file == "":
        exit(0)

    if "xlsx" not in file:
        c = tkinter.messagebox.showerror('Sample file generator ver2.0',
                                         '変換定義書ではありません。')
        exit(0)

    wb = xlrd.open_workbook(file)

    for page in range(wb.nsheets):
        sheet = wb.sheet_by_index(page)
        if sheet.name != "項目情報" and sheet.name != "基本情報":
            continue

        if sheet.name == "項目情報":
            infiles, join_info = read.reading_file_koumoku(sheet)
            sort_list = read.sorted_list(infiles)

        if sheet.name == "基本情報":
            basic_info_list = read.reading_file_kihon(sheet)

    write.generate_file(basic_info_list, sort_list, join_info, file)



    exit(0)


if __name__ == "__main__":
    main()