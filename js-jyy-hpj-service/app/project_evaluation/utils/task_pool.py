from concurrent.futures import ThreadPoolExecutor, wait

from app.project_evaluation.utils.evaluate import Evaluate
from app.project_evaluation.utils.calculation import TargetCalculation


class TaskPool:

    thread_pool = ThreadPoolExecutor(8)

    @staticmethod
    def do_calculation_and_evaluation(wbs_code):
        TargetCalculation(wbs_code).do_project_target_calculation()
        Evaluate(wbs_code).do_project_target_evaluate()

    @staticmethod
    def add_calculation_and_evaluation_job(wbs_code):
        return TaskPool.thread_pool.submit(TaskPool.do_calculation_and_evaluation, wbs_code)

    @staticmethod
    def wait_evaluation_target_job_finished(target_list, project_filed):
        job_list = []
        for target in target_list:
            job = TaskPool.thread_pool.submit(Evaluate.evaluate_target, target, project_filed)
            job_list.append(job)
        wait(job_list, 30)

    @staticmethod
    def wait_evaluation_target_aggregate_job_finished(target_list, project_filed):
        job_list = []
        for target in target_list:
            job = TaskPool.thread_pool.submit(Evaluate.evaluate_target_aggregate, target, project_filed)
            job_list.append(job)
        wait(job_list, 30)
