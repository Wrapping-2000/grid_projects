from mongoengine.queryset.visitor import Q
from app.project_evaluation.manager.models import Target


class TargetManager:

    @staticmethod
    def get_targets(wbs_code, target_name=None, year=None):
        q = Q(wbs_code=wbs_code)
        if target_name:
            q = Q(name=target_name) & q
        if year:
            q = ((Q(year__ne=None) & Q(year=year)) | Q(year=None)) & q

        return Target.objects(q)

    @staticmethod
    def delete_target(wbs_code):
        return Target.objects(wbs_code=wbs_code).delete()

    @staticmethod
    def get_project_target_year_list(wbs_code):
        return Target.objects(wbs_code=wbs_code).distinct("year")

    @staticmethod
    def get_max_project_target_year(wbs_code):
        year_list = TargetManager.get_project_target_year_list(wbs_code)
        if year_list:
            return max(year_list)

        return None

    @staticmethod
    def get_target_year_list(target_name):
        return Target.objects(name=target_name).distinct("year")

    @staticmethod
    def get_max_target_year(target_name):
        year_list = TargetManager.get_target_year_list(target_name)
        if year_list:
            return max(year_list)

        return None

    @staticmethod
    def add_target(target):
        # TODO 修改为upsert
        wbs_code = target.wbs_code
        name = target.name
        component_name = target.component_name
        year = target.year
        new_target = Target.objects(wbs_code=wbs_code,
                                    name=name,
                                    component_name=component_name,
                                    year=year).first()
        if not new_target:
            new_target = Target(wbs_code=wbs_code,
                                name=name,
                                component_name=component_name,
                                year=year)

        new_target.value = target.value
        new_target.data_raw = target.data_raw
        new_target.status = target.status

        new_target.validate()
        new_target.save()

