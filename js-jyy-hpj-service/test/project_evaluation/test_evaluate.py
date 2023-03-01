from app.project_evaluation.utils.evaluate import Evaluate
from test.test_basics import BasicsTestCase
from app.project_evaluation.manager import TargetManager
from app.project_evaluation.manager import ProjectManager
from app.project_evaluation.utils.target_utils import target_status


class EvaluateTestCase(BasicsTestCase):

    def test_evaluate_target_single_value(self):
        target = TargetManager.get_targets("13100114006B", "投资回收期（年）")[0]
        target = Evaluate.evaluate_target(target)

        print(target)
        # self.assertTrue(isinstance(target["average"], float))

    def test_evaluate_target_continuous_value(self):
        target = TargetManager.get_targets("1510A01506FH", "供（输）送电量（万kWh）")[1]
        target = Evaluate.evaluate_target(target)

        print(target)
        # self.assertTrue(isinstance(target["average"], float))

    def test_evaluate_target_component_continuous_value(self):
        target = TargetManager.get_targets("1510A01506FH", "线路平均负载率（%）")[0]
        target = Evaluate.evaluate_target(target)

        print(target)

        # self.assertTrue("year" in average and "value" in average)

    def test_get_average(self):
        # target = TargetManager.get_targets("1510A01506FH", "变电工程单站建场费（万元）")[0]
        # target = Evaluate.get_average(target, "classification")

        # target = TargetManager.get_targets("1510A01506FH", "单位线路长度增输电量（万kWh/公里）", 2020)[0]
        # target = Evaluate.get_average(target, "classification")

        target = TargetManager.get_targets("1510A01506FH", "线路平均负载率（%）", 2020)[0]
        target = Evaluate.get_average(target, "classification")

        print(target.average)
        print(target.value_list)
        print(target.average_list)

    def test_evaluate(self):
        for project in ProjectManager.get_project_list_all():
            Evaluate(project.wbs_code).do_project_target_evaluate()

