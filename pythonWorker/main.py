from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.configuration.configuration import Configuration
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.worker.worker import Worker

#### Add these lines if running on a mac####
from multiprocessing import set_start_method

# Import our own worker
from worker import SimplePythonWorker


set_start_method('fork')
############################################

SERVER_API_URL = 'https://play.orkes.io/api'
KEY_ID = '4af1da52-28d5-489c-b9b1-b7ffc32a0fe8'
KEY_SECRET = 'fLm9JZ1d5pnBxmtOXnaGiea6u84SQ1u8TaNvxjwx2FcHdCDS'

configuration = Configuration(
    server_api_url=SERVER_API_URL,
    debug=True,
    authentication_settings=AuthenticationSettings(
        key_id=KEY_ID,
        key_secret=KEY_SECRET
    ),
)

workers = [
    SimplePythonWorker(
        task_definition_name='DoThign',
    ),
    # SimplePythonWorker(
    #     task_definition_name="BarBouncer",
    # ),
    # Worker(
    #     task_definition_name='DoThign',
    #     execute_function=SimplePythonWorker.execute,
    #     poll_interval=1,
    # ),
    # Worker(
    #     task_definition_name='BarBouncer',
    #     execute_function=RandomFunction(),
    #     poll_interval=250,
    #     domain='test'
    # )
]

# If there are decorated workers in your application, scan_for_annotated_workers should be set
# default value of scan_for_annotated_workers is False
with TaskHandler(workers, configuration, scan_for_annotated_workers=False) as task_handler:
    print("starting processes")
    for worker in workers:
        print(worker.task_definition_name)
    task_handler.start_processes()
    input("Press enter to exit")
    print("ended processes")

# from conductor.client.worker.worker_task import WorkerTask
# 
# @WorkerTask(task_definition_name='python_annotated_task', worker_id='decorated', poll_interval=200.0)
# def python_annotated_task(input) -> object:
#     return {'message': 'python is so cool :)'}