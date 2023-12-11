import logging

from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models import Task, TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)
class SimplePythonWorker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        print("test")
        logger.debug("test")
        print(task.input_data)
        isOver18 = task.input_data["Age"] > 18
        logger.debug(f"IsOver18 calculation: {isOver18}")
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('worker_style', 'class')
        task_result.add_output_data('secret_number', 1234)
        task_result.add_output_data('is_it_true', False)
        task_result.add_output_data('IsOver18', isOver18)
        task_result.add_output_data("test", "test works")
        task_result.status = TaskResultStatus.COMPLETED
        return task_result

    def get_polling_interval_in_seconds(self) -> float:
        # poll every 500ms
        return 0.5