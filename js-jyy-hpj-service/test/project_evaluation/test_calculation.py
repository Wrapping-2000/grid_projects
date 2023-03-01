from app.project_evaluation.utils.calculation import TargetCalculation
from app.project_evaluation.manager import ProjectManager
from test.test_basics import BasicsTestCase


class TargetCalculationTestCase(BasicsTestCase):

    def test_calculation(self):
        for project in ProjectManager.get_project_list_all():
            TargetCalculation(project.wbs_code).do_project_target_calculation()


