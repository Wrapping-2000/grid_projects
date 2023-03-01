from app.project_evaluation.manager.models import ProjectDetail
from app.project_evaluation.utils import combine_year_list


class ProjectDetailManager:

    @staticmethod
    def get_project_detail(wbs_code):
        return ProjectDetail.objects(wbs_code=wbs_code).first()

    @staticmethod
    def delete_project_detail(wbs_code):
        return ProjectDetail.objects(wbs_code=wbs_code).delete()

    @staticmethod
    def get_project_detail_dict(wbs_code):
        result = {}
        project_detail = ProjectDetail.objects(wbs_code=wbs_code).first()

        for item in project_detail:
            result[item] = project_detail[item]

        return result

    @staticmethod
    def add_project_detail(wbs_code, params):
        project_detail = ProjectDetailManager.get_project_detail(wbs_code)
        if not project_detail:
            project_detail = ProjectDetail(wbs_code=wbs_code)
        for name in params:
            old_value = project_detail[name.strip()] if name.strip() in project_detail else None
            new_value = params[name]

            combine_value = combine_year_list(old_value, new_value)
            if combine_value:
                new_value = combine_value

            project_detail[name.strip()] = new_value

        project_detail.validate()
        project_detail.save()
