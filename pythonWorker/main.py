from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.configuration.configuration import Configuration
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.worker.worker import Worker

#### Add these lines if running on a mac####
from multiprocessing import set_start_method

# Import our own worker
from worker import SimplePythonWorker
from moreWorkers import *


set_start_method('fork')
############################################

SERVER_API_URL = 'http://localhost:8080/api'
KEY_ID = '<KEY_ID>'
KEY_SECRET = '<KEY_SECRET>'

configuration = Configuration(
    server_api_url=SERVER_API_URL,
    debug=True,
    authentication_settings=AuthenticationSettings(
        key_id=KEY_ID,
        key_secret=KEY_SECRET
    ),
)

workers = [
    ClassWorker(
        task_definition_name='python_task_example',
    ),
    # Worker(
    #     task_definition_name='python_execute_function_task',
    #     execute_function=SimplePythonWorker.execute,
    #     poll_interval=250,
    #     domain='test'
    # )
]

# If there are decorated workers in your application, scan_for_annotated_workers should be set
# default value of scan_for_annotated_workers is False
with TaskHandler(workers, configuration, scan_for_annotated_workers=True) as task_handler:
    print("starting processes")
    for worker in workers:
        print(worker.task_definition_name)
    task_handler.start_processes()
    print("ended processes")

from conductor.client.worker.worker_task import WorkerTask

@WorkerTask(task_definition_name='python_annotated_task', worker_id='decorated', poll_interval=200.0)
def python_annotated_task(input) -> object:
    return {'message': 'python is so cool :)'}