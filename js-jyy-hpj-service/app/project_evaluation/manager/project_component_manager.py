from app.project_evaluation.manager.models import ProjectComponent
from app.project_evaluation.utils import combine_year_list


class ProjectComponentManager:

    @staticmethod
    def get_project_component_list(wbs_code):
        return ProjectComponent.objects(wbs_code=wbs_code)

    @staticmethod
    def delete_project_component(wbs_code):
        return ProjectComponent.objects(wbs_code=wbs_code).delete()

    @staticmethod
    def get_project_component_dict_list(wbs_code):
        result = []
        for component in ProjectComponentManager.get_project_component_list(wbs_code):
            item = {}
            for name in component:
                item[name] = component[name]
            result.append(item)

        return result

    @staticmethod
    def get_component_target(wbs_code, target_name_list=tuple()):
        result = {}
        component_list = ProjectComponentManager.get_project_component_dict_list(wbs_code)
        for target_name in target_name_list:
            result[target_name] = [{
                "name": component["name"],
                "data": component.get(target_name)
            } for component in component_list]

        return result

    @staticmethod
    def get_project_component(name, wbs_code):
        return ProjectComponent.objects(name=name, wbs_code=wbs_code).first()

    @staticmethod
    def add_project_component(wbs_code, name, params):
        wbs_code = str(wbs_code).strip()
        name = str(name).strip()

        project_component = ProjectComponentManager.get_project_component(name, wbs_code)
        if not project_component:
            project_component = ProjectComponent(wbs_code=wbs_code, name=name)
        for name in params:
            old_value = project_component[name.strip()] if name.strip() in project_component else None
            new_value = params[name]

            combine_value = combine_year_list(old_value, new_value)
            if combine_value:
                new_value = combine_value

            project_component[name.strip()] = new_value

        project_component.validate()
        project_component.save()
