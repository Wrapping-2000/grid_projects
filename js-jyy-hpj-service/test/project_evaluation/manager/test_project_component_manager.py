from test.test_basics import BasicsTestCase
from app.project_evaluation.manager import ProjectComponentManager


class ProjectComponentManagerTestCase(BasicsTestCase):

    def test_delete(self):
        t = ProjectComponentManager.get_project_component_list("1310K016002M")

        print(t.delete())
