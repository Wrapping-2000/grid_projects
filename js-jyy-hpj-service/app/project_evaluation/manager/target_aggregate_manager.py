from app.project_evaluation.manager.models import Target
from app.project_evaluation.utils import average
from app.project_evaluation.utils import keep_2f


class TargetAggregateManager:

    target_project_pipeline = [
        {
            "$lookup": {
                "from": "project",
                "localField": "wbs_code",
                "foreignField": "wbs_code",
                "as": "project"
            }
        },
        {
            "$unwind": {
                "path": "$project"
            }
        }
    ]

    @staticmethod
    def get_statistics(query_raw):
        pipeline = TargetAggregateManager.target_project_pipeline.copy()
        pipeline.extend([
            {
                "$match": query_raw
            },
            {
                "$project": {"value": 1}
            }
        ])
        result = []
        for value in Target.objects().aggregate(pipeline):
            result.append(value)

        return result

    @staticmethod
    def get_target_average_value(target_name, project_filed, project_value):
        pipeline = TargetAggregateManager.target_project_pipeline.copy()
        pipeline.extend([
            {
                "$match": {"name": target_name, project_filed: project_value}
            },
            {
                "$group": {"_id": "1", "value": {"$avg": "$value"}}
            }
        ])
        for item in Target.objects().aggregate(pipeline):
            return item["value"]

    @staticmethod
    def get_target_year_average_value(target_name, project_filed, project_value):
        value_list = []
        pipeline = TargetAggregateManager.target_project_pipeline.copy()
        pipeline.extend([
            {
                "$match": {"name": target_name, project_filed: project_value}
            },
            {
                "$group": {"_id": "$year", "value_list": {"$push": "$value"}}
            }
        ])
        for item in Target.objects().aggregate(pipeline):
            value_list.append(
                {
                    "year": item["_id"],
                    "value": average(item["value_list"])
                }
            )
        return value_list

    @staticmethod
    def get_target_component_year_value(wbs_code, target_name, component_name):
        value_list = []
        match = {"name": target_name, "project.wbs_code": wbs_code}
        if component_name:
            match["component_name"] = component_name
        pipeline = TargetAggregateManager.target_project_pipeline.copy()
        pipeline.extend([
            {
                "$match": match
            },
            {
                "$project": {"year": 1, "value": 1}
            }
        ])

        for item in Target.objects().aggregate(pipeline):
            value_list.append(
                {
                    "year": item["year"],
                    "value": item["value"]
                }
            )
        return value_list

    @staticmethod
    def get_statistics(query_raw):
        value_list = []
        pipeline = TargetAggregateManager.target_project_pipeline.copy()
        pipeline.extend([
            {
                "$match": query_raw
            },
            {
                "$group": {"_id": "1", "value_list": {"$push": "$value"}}
            }
        ])
        for item in Target.objects().aggregate(pipeline):
            value_list = item["value_list"]

        return value_list

    @staticmethod
    def get_contrast_filed_target_average_value(target_name, contrast_filed):
        contrast_filed = "$project." + contrast_filed
        result = []
        pipeline = TargetAggregateManager.target_project_pipeline.copy()
        pipeline.extend([
            {
                "$match": {"name": target_name}
            },
            {
                "$group": {"_id": contrast_filed, "value": {"$avg": "$value"}}
            }
        ])
        for item in Target.objects().aggregate(pipeline):
            result.append(
                {
                    "name": item["_id"],
                    "value": keep_2f(item["value"])
                }
            )
        return result

    @staticmethod
    def get_contrast_filed_continuous_target_average_value(target_name, contrast_filed):
        contrast_filed = "$project." + contrast_filed
        result = []
        pipeline = TargetAggregateManager.target_project_pipeline.copy()
        pipeline.extend([
            {
                "$match": {"name": target_name}
            },
            {
                "$group": {"_id": {"index": contrast_filed, "year": "$year"}, "average": {"$avg": "$value"}}
            },
            {
                "$group": {"_id": "$_id.year", "value_item_list":
                    {"$push": {"name": "$_id.index", "value": "$average"}}}
            }
        ])
        for item in Target.objects().aggregate(pipeline):
            for value_item in item["value_item_list"]:
                value_item["value"] = keep_2f(value_item["value"])

            result.append(
                {
                    "year": item["_id"],
                    "value": item["value_item_list"]
                }
            )
        result.sort(key=lambda data: data["year"])
        return result

    @staticmethod
    def aggregate(name, contrast_filed, is_continuous_value=False):
        if not is_continuous_value:
            return TargetAggregateManager.get_contrast_filed_target_average_value(name, contrast_filed)
        else:
            return TargetAggregateManager.get_contrast_filed_continuous_target_average_value(name, contrast_filed)
