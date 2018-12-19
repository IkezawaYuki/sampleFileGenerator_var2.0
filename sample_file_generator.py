import csv
from _datetime import datetime
import xlrd
import os
import tkinter.filedialog
import tkinter.messagebox
import logging

import model.reading as read
import model.writing as write
import model.checking as check

h = logging.FileHandler("sample_file_generator.log", encoding="utf-8")
logger = logging.getLogger(__name__)
fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s :%(message)s")
h.setFormatter(fmt)
logger.setLevel(logging.DEBUG)
logger.addHandler(h)


def main():
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("", "*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file = tkinter.filedialog.askopenfilenames(filetypes=fTyp, initialdir=iDir)
    # file = "/Users/ikezaway/Downloads/test_data/IF03100099.xlsx"

    if file == "":
        exit(0)

    if type(file) is tuple:
        for f in file:
            if "xls" not in f:
                logger.info(f, " is not data hub.")
                tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                             '以下のファイルは変換定義書ではありません。\n' + f)
                continue
            logger.info(f)
            execute(f)
    else:
        if "xls" not in file:
             tkinter.messagebox.showerror('inspect -sample file generator ver3.0-','変換定義書ではありません。')
             logger.info(file, " is not data hub.")
             exit(1)
        logger.info(file, " is processing...")
        execute(file)

    logger.info(f, "is success.")
    tkinter.messagebox.showinfo('inspect -sample file generator ver3.0-',
                                '処理が正常終了しました。')
    exit(0)


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
            if check_result is False:
                tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                             '以下の変換定義書の「変換詳細情報」を確認してください。\n' + file)
    if check_result is True:
        write.generate_file(basic_info_list, sort_list, join_info, file)
    return True


if __name__ == "__main__":
    main()
