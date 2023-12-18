import uuid

from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.configuration.configuration import Configuration
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.worker.worker import Worker

#### Add these lines if running on a mac####
from multiprocessing import set_start_method

# Import our own worker
from worker import SimplePythonWorker, BarBouncer, MockEnquiryWorkers, SearchWorkers

set_start_method('fork')
############################################

SERVER_API_URL = 'https://play.orkes.io/api'
KEY_ID = "4af1da52-28d5-489c-b9b1-b7ffc32a0fe8"
KEY_SECRET = "fLm9JZ1d5pnBxmtOXnaGiea6u84SQ1u8TaNvxjwx2FcHdCDS"

configuration = Configuration(
    server_api_url=SERVER_API_URL,
    debug=True,
    authentication_settings=AuthenticationSettings(
        key_id=KEY_ID,
        key_secret=KEY_SECRET
    ),
)

workers = [
    # SimplePythonWorker(
    #     task_definition_name='CheckIsOver18',
    # ),
    # BarBouncer(
    #     task_definition_name='WelcomeToBar'
    # )
    # Worker(
    #     task_definition_name='CheckIsOver18',
    #     execute_function=SimplePythonWorker.is_over_18_using_task_input,
    #     poll_interval=1,
    #     #domain='test' # Not sure what this does yet
    # ),
    Worker(
        task_definition_name='initialise_enquiry',
        execute_function=MockEnquiryWorkers.execute_initialise_enquiry,
        poll_interval=1,
        #domain='test' # Not sure what this does yet
    ),
    Worker(
        task_definition_name='search_generator',
        execute_function=MockEnquiryWorkers.execute_search_generator,
        poll_interval=1,
        #domain='test' # Not sure what this does yet
    ),
    Worker(
        task_definition_name='google_search',
        execute_function=SearchWorkers.execute_google_search,
        poll_interval=1,
        #domain='test' # Not sure what this does yet
    ),
    Worker(
        task_definition_name='sayari_search',
        execute_function=SearchWorkers.execute_sayari_search,
        poll_interval=1,
        #domain='test' # Not sure what this does yet
    ),
    Worker(
        task_definition_name='nubela_search',
        execute_function=SearchWorkers.execute_nubela_search,
        poll_interval=1,
        #domain='test' # Not sure what this does yet
    ),
    Worker(
        task_definition_name='open_corporates_search',
        execute_function=SearchWorkers.execute_open_corporates_search,
        poll_interval=1,
        #domain='test' # Not sure what this does yet
    ),
    Worker(
        task_definition_name='companies_house_search',
        execute_function=SearchWorkers.execute_companies_house_search,
        poll_interval=1,
        #domain='test' # Not sure what this does yet
    ),
    # Worker(
    #     task_definition_name='companieshouse_search',   # expect: Failed to poll task
    #     execute_function=SearchWorkers.execute_companies_house_search,
    #     poll_interval=1,
    #     #domain='test' # Not sure what this does yet
    # )
    Worker(
        task_definition_name='google_convert',
        execute_function=SearchWorkers.execute_google_convert_search,
        poll_interval=1,
        #domain='test' # Not sure what this does yet
    ),
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

# @WorkerTask(task_definition_name='python_annotated_task', worker_id='decorated', poll_interval=200.0)
# def python_annotated_task(input) -> object:
#     return {'message': 'python is so cool :)'}

# Here is another way to make a function execute as a task. Avoids the faff of wrapping in Worker.
# Probably the one we want to use most ?
# @WorkerTask(task_definition_name='CheckIsOver18', worker_id='decorated', poll_interval=1.0)
# def is_over_18_using_input_object(task_input) -> dict[str, bool]:
#     age = task_input['Age']
#     isover18 = True if age > 18 else False
#     result = {"IsOver18": isover18}
#     return result