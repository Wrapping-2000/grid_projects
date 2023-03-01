from test.test_basics import BasicsTestCase

from app.project_evaluation.manager import TargetManager
from app.project_evaluation.manager.models import Target


class TargetManagerTestCase(BasicsTestCase):

    BasicsTestCase().setUp()

    def test_add_target(self):
        target = Target(
            name="影响电能质量考核次数（次）",
            wbs_code="1510701600Y7",
            year=2019,
            value=1.0,
            data_raw="{}"
        )
        TargetManager.add_target(target)
