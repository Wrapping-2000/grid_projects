from app.project_evaluation.utils.data_parser import DataParser
from test.test_basics import BasicsTestCase
from io import BytesIO


class DataParserTestCase(BasicsTestCase):

    def test_parse_new_project(self):
        # 2021年数据
        with open(r"C:\Users\hangzhang2\Desktop\项目\后评价\项目后评价资料包\2021年数据\2021年江苏项目后评价数据0805最终上报.xlsx",
                  "rb") as new_project_file:
            DataParser().parse_new_project(BytesIO(new_project_file.read()))
        # 2020年数据
        with open(r"C:\Users\hangzhang2\Desktop\项目\后评价\项目后评价资料包\2020年数据\【新增工程，含表8】2020年项目后评价数据汇总报系统（国网江苏电力0514）.xlsx",
                  "rb") as new_project_file:
            DataParser().parse_new_project(BytesIO(new_project_file.read()))
        # 2019年数据新增项目
        with open(r"C:\Users\hangzhang2\Desktop\项目\后评价\项目后评价资料包\2019年数据\2019-06-20-江苏公司_项目数据表修改版2019.6.20-新增项目-各专家已审核.xlsx",
                  "rb") as new_project_file:
            DataParser().parse_new_project(BytesIO(new_project_file.read()))
        # 2019回头看项目
        with open(r"C:\Users\hangzhang2\Desktop\项目\后评价\项目后评价资料包\2019年数据\2019-06-20-江苏公司_项目数据表修改版2019.6.20-回头看项目-各专家已审核.xlsx",
                  "rb") as new_project_file:
            DataParser().parse_new_project(BytesIO(new_project_file.read()))

    def test_parse_old_project(self):
        # 2021年数据
        with open(r"C:\Users\hangzhang2\Desktop\项目\后评价\项目后评价资料包\2021年数据\2021年江苏省电力公司投资效益数据-收资表2021.6 （-1提交系统）.xlsx",
                  "rb") as old_project_file:
            DataParser().parse_old_project(BytesIO(old_project_file.read()))
        # 2020年数据
        with open(r"C:\Users\hangzhang2\Desktop\项目\后评价\项目后评价资料包\2020年数据\【回头看数据】2019江苏省电力公司投资效益数据-汇总上报.xlsx",
                  "rb") as old_project_file:
            DataParser().parse_old_project(BytesIO(old_project_file.read()))
