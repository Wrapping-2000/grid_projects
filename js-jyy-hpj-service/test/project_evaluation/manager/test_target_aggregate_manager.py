from app.project_evaluation.manager import TargetAggregateManager
from test.test_basics import BasicsTestCase


class TargetAggregateManagerTestCase(BasicsTestCase):

    def test_get_contrast_filed_target_average_value(self):
        t = TargetAggregateManager.get_contrast_filed_target_average_value("影响电能质量考核次数（次）", "classification")
        print(t)

    def test_get_contrast_filed_continuous_target_average_value(self):
        t = TargetAggregateManager.get_contrast_filed_continuous_target_average_value("线路平均负载率（%）", "classification")
        print(t)

    def test_get_project_list_view(self):
        total, result = TargetAggregateManager.get_project_list_view({"name": "影响电能质量考核次数（次）"}, skip=20, limit=10)
        print(total)
        print(len(result))

    def test_get_statistics(self):
        value_list = TargetAggregateManager.get_statistics({"name": "线路最大负载率（%）"})
        boundary = [(0, 20), (20, 80), (80, "Infinity")]

        result = TargetAggregateManager.get_statistics_view(boundary, value_list)
        print(result)
