from app.project_evaluation.manager import TargetAggregateManager
from app.project_evaluation.manager.models import Target
from app.project_evaluation.utils.task_pool import TaskPool


class TargetViewsManager:

    @staticmethod
    def get_project_list_view(query_raw, contrast_filed, limit=10, skip=0):
        pipeline = TargetAggregateManager.target_project_pipeline.copy()
        pipeline.extend([
            {
                "$match": query_raw
            },
            {
                "$sort": {"project.operation_year": -1}
            },
            {
                "$skip": skip
            },
            {
                "$limit": limit
            }
        ])

        result = []
        target_list = [target for target in Target.objects().aggregate(pipeline)]
        TaskPool.wait_evaluation_target_aggregate_job_finished(target_list, contrast_filed)

        for item in target_list:
            item_view = {
                "project_name": item["project"]["name"],
                "voltage_level": item["project"]["voltage_level"],
                "classification": item["project"]["classification"],
                "operation_year": item["project"]["operation_year"],
                "company": item["project"]["company"],
                "value": item["value"],
                "status": item["status"].get("color", None) if item.get("status") else None,
                "status_msg": item["status"].get("message", None) if item.get("status") else None,
                "target_year": item.get("year"),
                "component_name": item.get("component_name"),
                "wbs_code": item.get("wbs_code"),
                "average": item.get("average")
            }
            result.append(item_view)

        total = 0
        pipeline = TargetAggregateManager.target_project_pipeline.copy()
        pipeline.extend([
            {
                "$match": query_raw
            },
            {
                "$count": "total"
            }
        ])
        for item in Target.objects().aggregate(pipeline):
            total = item["total"]

        return total, result

    @staticmethod
    def get_statistics_view(boundary, value_list):
        boundary_map = {}
        for value_boundary in boundary:
            boundary_map.setdefault(value_boundary, 0)

        for new_value in value_list:
            for (start, end), value in boundary_map.items():
                if start == "-Infinity":
                    if new_value < end:
                        boundary_map[(start, end)] = value + 1
                elif end == "Infinity":
                    if new_value >= start:
                        boundary_map[(start, end)] = value + 1
                elif start <= new_value < end:
                    boundary_map[(start, end)] = value + 1

        result = []
        for (start, end), total in boundary_map.items():
            result.append(
                {
                    "start": start,
                    "end": end,
                    "count": total
                }
            )
        return result
