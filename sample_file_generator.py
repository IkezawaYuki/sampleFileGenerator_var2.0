import csv
from _datetime import datetime
import xlrd
import os
import tkinter.filedialog
import tkinter.messagebox
import logging
import sys

import model.reading as read
import model.writing as write
import model.checking as check

import generator_config as l


def main():
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("", "*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file = tkinter.filedialog.askopenfilenames(filetypes=fTyp, initialdir=iDir)

    if file == "":
        sys.exit(0)

    if type(file) is tuple:
        for f in file:
            if "xls" not in f:
                l.logger.error(f + " is not Data hub.")
                tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                             '以下のファイルは変換定義書ではありません。\n' + f)
                sys.exit(1)
            execute(f)
    else:
        if "xls" not in file:
             l.logger.error(file + " is not Data hub.")
             tkinter.messagebox.showerror('inspect -sample file generator ver3.0-','変換定義書ではありません。')
             sys.exit(1)
        execute(file)

    l.logger.info("Execute is success.")
    tkinter.messagebox.showinfo('inspect -sample file generator ver3.0-',
                                '正常終了しました。\n無限ループ、デッドコード、NullPointerExceptionの可能性はありません。'
                                '\n\nサンプルファイルを作成しました。')
    sys.exit(0)


def execute(file):
    wb = xlrd.open_workbook(file)
    basic_info_list = []
    join_info = []
    sort_list = []
    check_result = False

    for page in range(wb.nsheets):
        sheet = wb.sheet_by_index(page)

        if sheet.name == "基本情報":
            basic_info_list = read.reading_file_kihon(sheet)

        if sheet.name == "項目情報":
            in_files, join_info = read.reading_file_koumoku(sheet)
            sort_list = read.sorted_list(in_files)

        if sheet.name == "変換詳細情報":
            check_result = check.execute_coverage_test(sheet)

    if check_result:
        write.generate_file(basic_info_list, sort_list, join_info, file)
    return True


if __name__ == "__main__":
    main()
