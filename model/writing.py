import os
import csv
import sys
import tkinter.messagebox
from _datetime import datetime


class FileInfo:
    """
    サンプルファイルのオブジェクト
    """
    def __init__(self):
        self.header = []
        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.data4 = []
        self.data5 = []
        self.data_kotei_1 = ""
        self.data_kotei_2 = ""
        self.data_kotei_3 = ""
        self.data_kotei_4 = ""
        self.data_kotei_5 = ""


def generate_file(basic_info_list, sort_list, join_info, file_path):
    target_file_path = create_output_folder(file_path)
    try:
        for i in range(len(sort_list)):
            sample = FileInfo()
            if basic_info_list[i][2] == "可変長":
                if join_info is not None:
                    sample = header_and_data_generate(sample, sort_list[i], join_info[i])
                else:
                    sample = header_and_data_generate(sample, sort_list[i], None)
                delimiter = sort_list[i][0][3]
            else:
                if join_info is not None:
                    sample = header_and_data_generate_ver_kotei(sample, sort_list[i], join_info[i])
                else:
                    sample = header_and_data_generate_ver_kotei(sample, sort_list[i], None)
                delimiter = None
            execute_write(basic_info_list[i], target_file_path, sample, delimiter)
    except IndexError:
        tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                     "一度環境に適用された変換定義書でないと、\n正しく情報を読み取れません。\n環境適用後、HUEからダウンロードしたものに使用してください。")
        sys.exit(0)


def execute_write(basic_info, file_path, sample, delimiter):
    """
    ファイルの出力が行われるメソッド。
    :param basic_info: 基本情報
    :param file_path: 出力先のパス
    :param sample: サンプルファイル
    :param delimiter: くくり文字
    :return:
    """
    file_name = file_path + basic_info[0] + "_sample.csv"
    encode_kind = adjust_encode_kind(basic_info[1])
    format_kind = basic_info[2]
    delimiter = delimiter
    header_flag = basic_info[5]

    if format_kind == "可変長":
        if not os.path.isdir(file_path):
            os.makedirs(file_path)

        if delimiter == '':
            with open(file_name, "w+", encoding=encode_kind, newline="") as f:
                writer = csv.writer(f, lineterminator='\n')
                if header_flag == "0" or header_flag == 0 or header_flag == 0.0 or header_flag == "0.0":
                    header_list = list(
                        map(lambda header: header + "<削除必須>", sample.header))
                    writer.writerow(header_list)
                else:
                    writer.writerow(sample.header)
                writer.writerow(sample.data1)
                writer.writerow(sample.data2)
                writer.writerow(sample.data3)
                writer.writerow(sample.data4)
                writer.writerow(sample.data5)
        else:
            with open(file_name, "w+", encoding=encode_kind, newline="", errors="replace") as f:
                writer = csv.writer(f, lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC)

                if header_flag == "0" or header_flag == 0 or header_flag == 0.0 or header_flag == "0.0":
                    header_list = list(
                        map(lambda header: header + "<削除必須>", sample.header))
                    writer.writerow(header_list)
                else:
                    writer.writerow(sample.header)
                writer.writerow(sample.data1)
                writer.writerow(sample.data2)
                writer.writerow(sample.data3)
                writer.writerow(sample.data4)
                writer.writerow(sample.data5)
    else:
        print(sample.data_kotei_1)
        tkinter.messagebox.showerror('inspect -sample file generator ver3.0-',
                                     "var3.0では固定長ファイルの出力はスキップします。")
        # with open(file_name, "w+", encoding=encode_kind, newline="") as f:


def adjust_encode_kind(encode_kind):
    if encode_kind == "UTF-8":
        return "utf-8"
    elif encode_kind == "MS932":
        return "shift_jis"
    elif encode_kind == "EUC-JP":
        return "EUC-JP"
    else:
        return "utf-8"


def create_output_folder(file_path):
    name, ext = os.path.splitext(file_path)
    date_data = datetime.now().strftime("%Y_%m%d")
    return name + "_" + date_data + "_sample/"


def get_row_info(row_info):
    start_byte = int(float(row_info[2]))
    end_byte = int(float(row_info[3]))
    right_or_left = row_info[4]
    filling_char = row_info[5]
    date_format = row_info[6]
    if right_or_left == "右詰め":
        right_or_left = ">"
    else:
        right_or_left = "<"

    if filling_char == "半角スペース":
        filling_char = " "
    elif filling_char == "全角スペース":
        filling_char = "　"

    return start_byte, end_byte, date_format, right_or_left, filling_char


def header_and_data_generate_ver_kotei(sample, in_file, join_info):
    """
    固定長のファイルのデータを作成するメソッド
    """
    item_count = 1
    byte_counter = 0
    temp = ""

    for row_info in in_file:
        start_byte, end_byte, date_format, right_or_left, filling_char = get_row_info(row_info)

        if start_byte != byte_counter + 1:
            for _ in range(byte_counter+1, start_byte):
                temp += "*"

        word = ""
        for _ in range(start_byte, end_byte+1):
            word += str(item_count)
        if date_format != "":
            date_data = adjust_date_format_ver_kotei(date_format)
            format_char = "{:" + right_or_left + filling_char + str(len(word)) + "}"
            word = format_char.format(date_data)

        temp += word
        item_count += 1
        byte_counter = end_byte

    sample.data_kotei_1 = temp
    sample.data_kotei_2 = temp
    sample.data_kotei_3 = temp
    sample.data_kotei_4 = temp
    sample.data_kotei_5 = temp

    return sample


def header_and_data_generate(sample, sort_list, join_info):
    """
    出力するサンプルファイルの内容を決定するメソッド
    :param sample: 出力するファイルごとのオブジェクト
    :param sort_list: 項目情報
    :param join_info: 結合情報
    :return: 情報を書き込んだ後のファイルオブジェクト
    """
    counter = 1
    for row_info in sort_list:
        colum_index = int(row_info[2])
        while counter < colum_index:
            sample.header.append("*****")
            sample.data1.append("*****")
            sample.data2.append("*****")
            sample.data3.append("*****")
            sample.data4.append("*****")
            sample.data5.append("*****")
            counter += 1

        header_info = row_info[1]
        sample.header.append(header_info)

        date_format = row_info[4]
        if date_format != "":
            adjust_date_format(sample, date_format)
            counter += 1
            continue

        if join_info is not None:
            if header_info in join_info[1]:
                sample.data1.append("key_1")
                sample.data2.append("key_2")
                sample.data3.append("key_3")
                sample.data4.append("key_4")
                sample.data5.append("key_5")
                counter += 1
                continue

        sample.data1.append("12345")
        sample.data2.append("12345")
        sample.data3.append("12345")
        sample.data4.append("12345")
        sample.data5.append("12345")
        counter += 1
    return sample


def adjust_date_format(sample, date_format):
    if date_format == "YYYY/MM/DD":
        day = datetime.now().strftime("%Y/%m/%d")
        sample.data1.append(str(day))
        sample.data2.append(str(day))
        sample.data3.append(str(day))
        sample.data4.append(str(day))
        sample.data5.append(str(day))
    elif date_format == "YYYYMMDD":
        day = datetime.now().strftime("%Y%m%d")
        sample.data1.append(str(day))
        sample.data2.append(str(day))
        sample.data3.append(str(day))
        sample.data4.append(str(day))
        sample.data5.append(str(day))
    elif date_format == "YYYYMM":
        day = datetime.now().strftime("%Y%m")
        sample.data1.append(str(day))
        sample.data2.append(str(day))
        sample.data3.append(str(day))
        sample.data4.append(str(day))
        sample.data5.append(str(day))
    elif date_format == "MMDD":
        day = datetime.now().strftime("%m%d")
        sample.data1.append(str(day))
        sample.data2.append(str(day))
        sample.data3.append(str(day))
        sample.data4.append(str(day))
        sample.data5.append(str(day))
    elif date_format == "YYYY/MM":
        day = datetime.now().strftime("%Y/%m")
        sample.data1.append(str(day))
        sample.data2.append(str(day))
        sample.data3.append(str(day))
        sample.data4.append(str(day))
        sample.data5.append(str(day))
    elif date_format == "MM/DD":
        day = datetime.now().strftime("%m/%d")
        sample.data1.append(str(day))
        sample.data2.append(str(day))
        sample.data3.append(str(day))
        sample.data4.append(str(day))
        sample.data5.append(str(day))
    elif date_format == "YYYY":
        day = datetime.now().strftime("%Y")
        sample.data1.append(str(day))
        sample.data2.append(str(day))
        sample.data3.append(str(day))
        sample.data4.append(str(day))
        sample.data5.append(str(day))
    elif date_format == "MM":
        day = datetime.now().strftime("%m")
        sample.data1.append(str(day))
        sample.data2.append(str(day))
        sample.data3.append(str(day))
        sample.data4.append(str(day))
        sample.data5.append(str(day))
    elif date_format == "DD":
        day = datetime.now().strftime("%d")
        sample.data1.append(str(day))
        sample.data2.append(str(day))
        sample.data3.append(str(day))
        sample.data4.append(str(day))
        sample.data5.append(str(day))


def adjust_date_format_ver_kotei(date_format):
    if date_format == "YYYY/MM/DD":
        day = datetime.now().strftime("%Y/%m/%d")
    elif date_format == "YYYYMMDD":
        day = datetime.now().strftime("%Y%m%d")
    elif date_format == "YYYYMM":
        day = datetime.now().strftime("%Y%m")
    elif date_format == "MMDD":
        day = datetime.now().strftime("%m%d")
    elif date_format == "YYYY/MM":
        day = datetime.now().strftime("%Y/%m")
    elif date_format == "MM/DD":
        day = datetime.now().strftime("%m/%d")
    elif date_format == "YYYY":
        day = datetime.now().strftime("%Y")
    elif date_format == "MM":
        day = datetime.now().strftime("%m")
    elif date_format == "DD":
        day = datetime.now().strftime("%d")

    return str(day)