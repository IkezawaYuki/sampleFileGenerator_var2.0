import model.reading as read
import model.writing as write
import sample_file_generator

class TestCase(object):
    def test_xstrs(self):
        info = None
        assert read.xstr(info) == ""

    def test_sorted_list(self):
        info = [[("3","3","3"),("2","2","2"),("4","4","4"),("1","1","1")]]
        assert read.sorted_list(info) == [[("1","1","1"),("2","2","2"),("3","3","3"),("4","4","4")]]

    def test_adjust_encode_king(self):
        info = "UTF-8"
        assert write.adjust_encode_kind(info) == "utf-8"

    def test_create_out_put_folder(self):
        info = "C:¥¥file¥fike¥faaa¥dddd"
        assert write.create_output_folder(info) == "C:¥¥file¥fike¥faaa¥dddd_20181008_sample/"

    def test_sample_file_generator(self):
        file = (
                    "/Users/ikezaway/Downloads/test_data/IF00100052.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF00100053.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF00100054.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF00100055.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF00100056.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF00100057.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF00100051.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF00100090.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF00100099.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF52700061.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF52700059.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF52700061.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF52700062.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF52700063.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF52700064.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF52700065.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF52700066.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF52700098.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF21000051.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF21000052.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF21000053.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF21000054.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF21000055.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF21000056.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF21000057.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF21000058.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF21000059.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF21000099.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF03200052.xls",
                    "/Users/ikezaway/Downloads/test_data/IF03200053.xls",
                    "/Users/ikezaway/Downloads/test_data/IF03200054.xls",
                    "/Users/ikezaway/Downloads/test_data/IF03200055.xls",
                    "/Users/ikezaway/Downloads/test_data/IF03200056.xls",
                    "/Users/ikezaway/Downloads/test_data/IF03200099.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF00120052.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF00120054.xlsx",
                    "/Users/ikezaway/Downloads/test_data/IF00120055.xlsx"

                 )
        for f in file:
            assert sample_file_generator.execute(f) is True
