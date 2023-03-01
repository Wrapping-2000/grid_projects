from app.project_evaluation.manager import ProjectManager
from test.test_basics import BasicsTestCase


class ProjectManagerTestCase(BasicsTestCase):

    def test_add_project(self):
        ProjectManager.add_project(name="沭阳600千伏输变电工程",
                                   wbs_code="1310K016002M",
                                   voltage_level=500,
                                   classification="满足用电需求",
                                   operation_year=2019,
                                   plan_year=2019,
                                   company_province="国网江苏省电力公司",
                                   company_city="国网泰州供电公司",
                                   company_county="国网高邮供电公司",
                                   energy_type="光伏",
                                   channel_type=None,
                                   budget=8411.3,
                                   capacitance=1064,
                                   wire_length=None,
                                   transmission_capacity=520
                                   )

        self.assertTrue(ProjectManager.get_project(wbs_code="1310K016002M") is not None)

    def test_get_project(self):
        project = ProjectManager.get_project(wbs_code="1310K016002M")
        self.assertTrue(project is not None)

    def test_get_object_list(self):
        project_list = ProjectManager.get_project_list()
        self.assertTrue(len(project_list) > 0)

    def test_count_project(self):
        count = ProjectManager.get_project_count()
        self.assertTrue(count > 1)

    def test_delete_project(self):
        ProjectManager.delete_project(wbs_code="1310K016002M")
        self.assertTrue(ProjectManager.get_project(wbs_code="1310K016002M") is None)

    def test_aggregation_filed(self):
        self.assertTrue(len(ProjectManager.get_voltage_level_list()) > 0)
        self.assertTrue(len(ProjectManager.get_classification_list()) > 0)
        self.assertTrue(len(ProjectManager.get_operation_year_list()) > 0)
