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
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)
        age = task_input['Age']
        isover18 = True if age > 18 else False
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('blah', 'omg it works')
        task_result.add_output_data('IsOver18', isover18)
        task_result.status = TaskResultStatus.COMPLETED
        return task_result

    def get_polling_interval_in_seconds(self) -> float:
        # poll every 500ms
        return 0.5


class BarBouncer(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)
        doThingResult = task_input['DoThignResult']
        isOver18 = doThingResult["IsOver18"]
        if isOver18:
            message = "Hello there! Take a nice cool refreshing beverage on the house!"
        else:
            message = "Please leave. I don't like you >:( You are TOO YOUNG!"
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data("BarGreetings", message)
        logger.debug("--------------Bar Bouncer happened!")
        task_result.status = TaskResultStatus.COMPLETED
        return task_result

    def get_polling_interval_in_seconds(self) -> float:
        # poll every 500ms
        return 0.5
