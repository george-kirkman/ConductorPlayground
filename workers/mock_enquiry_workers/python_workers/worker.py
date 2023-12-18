import logging
from enum import Enum
import uuid

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

    # Here we're exploring the different kinds of functions that can go in the Worker `execute_function` parameter.
    # They have to be static methods - don't necessarily need to be in a class (all functions outside of classes are already static)
    # but might be nice for grouping etc.
    @staticmethod
    def is_over_18_using_task_input(task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)
        age = task_input['Age']
        isover18 = True if age > 18 else False
        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )
        task_result.add_output_data("IsOver18", isover18)
        task_result.status = TaskResultStatus.COMPLETED
        return task_result

    # THIS ONE DOES NOT WORK¬!!!!! CONDUCT|oR STOOPID 
    # worker/worker.py Line 68 doesn't use the correct input.
    # should be task_result.output_data = self.execute_function(execute_function_input)

    # So for now, we're gonna avoid this usage. Might raise a PR! :)
    @staticmethod
    def is_over_18_using_input_object(task_input) -> dict[str, bool]:
        logger.debug("-------- input: ")
        logger.debug(task_input)
        age = task_input['Age']
        isover18 = True if age > 18 else False
        result = {"IsOver18": isover18}
        return result

    def get_polling_interval_in_seconds(self) -> float:
        # poll every 500ms
        return 0.5


class BarBouncer(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)
        isover18_result = task_input["IsOver18"]
        isOver18 = isover18_result["IsOver18"]
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


# -----------------------------------------
# MOCK ENQUIRY EXECUTION FUNCTIONS


class DataProvider(Enum):
    NUBELA = 'Nubela'
    GOOGLE = 'Google'
    SAYARI = 'Sayari'
    OPENCORPORATES = 'OpenCorporates'
    COMPANIESHOUSE = 'CompaniesHouse'


class EntityType(Enum):
    PERSON = 'Person'
    ORGANISATION = 'Organisation'


class Subject:
    def __init__(self, item: str, type: str):
        self.item = item
        self.type = type

    def to_dict(self):
        return {"item": self.item, "type": self.type}


class Context:
    def __init__(self, item: str, type: str):
        self.item = item
        self.type = type

    def to_dict(self):
        return {"item": self.item, "type": self.type}


class EnquiryMetadata:
    def __init__(self, enquiry_id: str, subject: Subject, context: Context):
        self.enquiry_id = enquiry_id
        self.subject = subject
        self.context = context  # may need to be list?

    def to_dict(self):
        return {
            "enquiry_id": self.enquiry_id,
            "subject": self.subject.to_dict(),
            "context": self.context.to_dict()
        }


# SEARCH WORKFLOWS
class GoogleSearchRequest:
    def __init__(self, query: str):
        self.query = query  # i.e. subject name + other informative strings to search on

    def to_dict(self):
        return {
            "query": self.query,
        }


class GoogleSearchOutput:
    def __init__(self, search_query: str, url: str, title: str, summary: str):
        self.search_query = search_query
        self.url = url
        self.title = title
        self.summary = summary

    def to_dict(self):
        return {
            "search_query": self.search_query,
            "url": self.url,
            "title": self.title,
            "summary": self.summary
        }


class SayariSearchRequest:
    def __init__(self, entity_name: str, entity_type: str):
        self.entity_name = entity_name
        self.entity_type = entity_type

    def to_dict(self):
        return {
            'entity_name': self.entity_name,
            'entity_type': self.entity_type
        }


class SayariSearchOutput:
    def __init__(self, entity_name: str, entity_type: str, url: str, title: str, summary: str):
        self.entity_name = entity_name
        self.entity_type = entity_type
        self.url = url
        self.title = title
        self.summary = summary


class NubelaSearchRequest:  # (linkedin)
    def __init__(self, entity_name: str, entity_type: str, entity_context: str):
        self.entity_name = entity_name
        self.entity_type = entity_type
        self.entity_context = entity_context

    def to_dict(self):
        return {
            'entity_name': self.entity_name,
            'entity_type': self.entity_type,
            'entity_context': self.entity_context
        }


class NubelaSearchOutput:
    def __init__(self, linkedin_search_string: str, url: str):
        self.linkedin_search_string = linkedin_search_string
        self.url = url


class OpenCorporatesSearchRequest:
    def __init__(self, entity_name: str, entity_context: str):
        self.entity_name = entity_name
        self.entity_context = entity_context

    def to_dict(self):
        return {
            'entity_name': self.entity_name,
            'entity_context': self.entity_context
        }


class CompaniesHouseSearchOutput:
    def __init__(self, ch_search_string: str, url: str, id: uuid):
        self.ch_search_string = ch_search_string
        self.url = url
        self.id = id


class CompaniesHouseSearchRequest:
    def __init__(self, entity_name: str, entity_context: str):
        self.entity_name = entity_name
        self.entity_context = entity_context

    def to_dict(self):
        return {
            'entity_name': self.entity_name,
            'entity_context': self.entity_context
        }


class OpenCorporatesSearchOutput:
    def __init__(self, oc_search_string: str, url: str, id: uuid):
        self.oc_search_string = oc_search_string
        self.url = url
        self.id = id


class MockEnquiryWorkers(WorkerInterface):
    @staticmethod
    def execute_initialise_enquiry(task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)

        enquiry_id = str(uuid.uuid4())
        subject = {'item': task_input['Subject'],
                   'type': 'Person'}
        context = {'item': task_input['Context'],
                   'type': 'Organisation'}

        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )
        task_result.add_output_data('enquiry_id', enquiry_id)
        task_result.add_output_data('subject', subject)
        task_result.add_output_data('context', context)
        task_result.status = TaskResultStatus.COMPLETED
        print("<--- INTIALISE-ENQUIRY TASK COMPLETE! --->")
        print(task_result.output_data)
        return task_result

    @staticmethod
    def execute_search_generator(task: Task) -> TaskResult:
        task_input = task.input_data
        enq_metadata = task_input['enquiry_metadata']
        logger.debug("-------- input: ")
        logger.debug(task_input)

        data_providers = ['Nubela',
                          'Google',
                          'Sayari',
                          'OpenCorporates',
                          'CompaniesHouse']
                          # 'Bing'] # created as test to hit: unexpected data provider terminate

        search_specs = []
        for data_provider in data_providers:
            search_name_context_request = enq_metadata['subject']['item'] + " " + enq_metadata['context']['item']
            if data_provider == "Google":   # or data_provider == "Bing":
                search_query = search_name_context_request
                search_request = GoogleSearchRequest(search_query).to_dict()
            elif data_provider == "Sayari":
                name = enq_metadata['subject']['item']
                type = enq_metadata['subject']['type']
                search_request = SayariSearchRequest(name, type).to_dict()
            elif data_provider == "Nubela":
                name = enq_metadata['subject']['item']
                type = enq_metadata['subject']['type']
                context = "" if enq_metadata['context']['type'] == "Person" else enq_metadata['context']['item']
                search_request = NubelaSearchRequest(name, type, context).to_dict()
            elif data_provider == "OpenCorporates":
                name = enq_metadata['subject']['item']
                context = enq_metadata['context']['item']
                search_request = OpenCorporatesSearchRequest(name, context).to_dict()
            elif data_provider == "CompaniesHouse":
                name = enq_metadata['subject']['item']
                context = enq_metadata['context']['item']
                search_request = CompaniesHouseSearchRequest(name, context).to_dict()
            # else:
                # TODO: log an error

            search_specs.append({
                "search_specification": {
                    # should be Enum: DataProvider
                    "data_provider": data_provider,
                    "search_request": search_request
                }
            })

        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )
        task_result.add_output_data('enquiry_metadata', enq_metadata)
        task_result.add_output_data('search_specifications', search_specs)
        task_result.status = TaskResultStatus.COMPLETED
        print("<--- SEARCH-GENERATOR TASK COMPLETE! --->")
        return task_result

    # TODO: Add report_gen execute function


class SearchWorkers(WorkerInterface):
    @staticmethod
    def execute_google_search(task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)

        input_search_spec = task_input['search_specification']
        input_search_query = input_search_spec['search_request']['query']
        # --- insert specific search logic here ---

        search_results = [
            {
                "search_query": input_search_query,
                "url": "https://www.lseg.com/en/about-us/executive-team",
                "title": "LSEG Executive Team",
                "summary": "David is CEO of London Stock Exchange Group (LSEG) and a member of the Board of LSEG plc."
                           "He joined the Group in August 2018, having spent 20 years at ..."
            },
            {
                "search_query": input_search_query,
                "url": "https://www.lsegissuerservices.com/spark/lse-whitepaper-trading-insights",
                "title": "Lifting the Lid on the Close",
                "summary": "Read the whitepaper by David A. Smith, Product Manager, London Stock Exchange, Secondary"
                           " Markets & Turquoise to find out about the latest ..."
            },
            {
                "search_query": input_search_query,
                "url": "https://docs.londonstockexchange.com/sites/default/files/documents/n1218.pdf",
                "title": "Market Notice",
                "summary": "Queries on the content of this notice should be addressed to David Smith, telephone +44 "
                           "(0)20 7797 1765 or by email dsmith@lseg.com. Denzil ..."
            }
        ]

        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )

        # TODO: add enquiry_metadata to search input
        # task_result.add_output_data('enquiry_metadata', task_input)
        task_result.add_output_data('search_results', search_results)
        task_result.status = TaskResultStatus.COMPLETED
        print("<--- GOOGLE-SEARCH TASK COMPLETE! --->")
        return task_result

    @staticmethod
    def execute_sayari_search(task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)

        input_search_spec = task_input['search_specification']
        input_search_request = input_search_spec['search_request']
        # --- insert specific search logic here ---

        search_results = [
            {
                "entity_name": input_search_request['entity_name'],
                "entity_type": input_search_request['entity_type'],
                "url": "https://theasset.com/article/20907/theasset.com",
                "title": "London Stock Exchange Group assumes control of FTSE ...",
                "summary": "David Lester, LSEG's director of information services and FTSE International ..."
                           " David Smith. senior investment director, Asian equities. abrdn."
            },
            {
                "entity_name": input_search_request['entity_name'],
                "entity_type": input_search_request['entity_type'],
                "url": "https://markets.ft.com/data/equities/tearsheet/summary?s: SMDS:LSE",
                "title": "DS Smith PLC, SMDS:LSE summary - FT.com - Markets data",
                "summary": "Latest DS Smith PLC (SMDS:LSE) share price with interactive charts, historical prices,"
                           " comparative analysis, forecasts, business profile and more."
            }
        ]

        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )

        task_result.add_output_data('search_results', search_results)
        task_result.status = TaskResultStatus.COMPLETED
        print("<--- SAYARI-SEARCH TASK COMPLETE! --->")
        return task_result

    @staticmethod
    def execute_nubela_search(task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)

        input_search_spec = task_input['search_specification']
        input_search_request = input_search_spec['search_request']
        # --- insert specific search logic here ---

        search_results = [
            {
                "linkedin_search_string": input_search_request['entity_name'] + ' ' + input_search_request['entity_context'],
                "url": "https://www.linkedin.com/in/david-smith-71b43713/?originalSubdomain=uk",
            },
        ]

        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )

        task_result.add_output_data('search_results', search_results)
        task_result.status = TaskResultStatus.COMPLETED
        print("<--- NUBELA-SEARCH TASK COMPLETE! --->")
        return task_result

    @staticmethod
    def execute_open_corporates_search(task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)

        input_search_spec = task_input['search_specification']
        input_search_request = input_search_spec['search_request']
        # --- insert specific search logic here ---

        search_results = [
            {
                "oc_search_string": input_search_request['entity_name'] + ' ' + input_search_request['entity_context'],
                "url": "https://opencorporates.com/officers/38135099",
                "id": str(uuid.uuid4())
            },
        ]

        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )

        task_result.add_output_data('search_results', search_results)
        task_result.status = TaskResultStatus.COMPLETED
        print("<--- OPENCORPORATES-SEARCH TASK COMPLETE! --->")
        return task_result

    @staticmethod
    def execute_companies_house_search(task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)

        input_search_spec = task_input['search_specification']
        input_search_request = input_search_spec['search_request']
        # --- insert specific search logic here ---

        search_results = [
            {
                "ch_search_string": input_search_request['entity_name'] + ' ' + input_search_request['entity_context'],
                "url": "https://find-and-update.company-information.service.gov.uk/company/00914878",
                "id": str(uuid.uuid4())
            },
        ]

        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )

        task_result.add_output_data('search_results', search_results)
        task_result.status = TaskResultStatus.COMPLETED
        print("<--- COMPANIESHOUSE-SEARCH TASK COMPLETE! --->")
        return task_result

    @staticmethod
    def execute_google_convert_search(task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)

        search_output = task_input['google_search_results']
        # --- insert specific search logic here ---
        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )
        # TODO: insert time sleep
        task_result.add_output_data('convert_results', search_output)
        task_result.status = TaskResultStatus.COMPLETED
        print("<--- GOOGLE-CONVERT TASK COMPLETE! --->")
        return task_result

    @staticmethod
    def execute_sayari_convert_search(task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)

        search_output = task_input['sayari_search_results']
        # --- insert specific search logic here ---
        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )
        # TODO: insert time sleep
        task_result.add_output_data('convert_results', search_output)
        task_result.status = TaskResultStatus.COMPLETED
        print("<--- SAYARI-CONVERT TASK COMPLETE! --->")
        return task_result

    @staticmethod
    def execute_nubela_convert_search(task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)

        search_output = task_input['nubela_search_results']
        # --- insert specific search logic here ---
        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )
        # TODO: insert time sleep
        task_result.add_output_data('convert_results', search_output)
        task_result.status = TaskResultStatus.COMPLETED
        print("<--- NUBELA-CONVERT TASK COMPLETE! --->")
        return task_result

    @staticmethod
    def execute_open_corporates_convert_search(task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)

        search_output = task_input['open_corporates_search_results']
        # --- insert specific search logic here ---
        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )
        # TODO: insert time sleep
        task_result.add_output_data('convert_results', search_output)
        task_result.status = TaskResultStatus.COMPLETED
        print("<--- OPEN-CORPORATES-CONVERT TASK COMPLETE! --->")
        return task_result

    @staticmethod
    def execute_companies_house_convert_search(task: Task) -> TaskResult:
        task_input = task.input_data
        logger.debug("-------- input: ")
        logger.debug(task_input)

        search_output = task_input['companies_house_search_results']
        # --- insert specific search logic here ---
        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id='your_custom_id'
        )
        # TODO: insert time sleep
        task_result.add_output_data('convert_results', search_output)
        task_result.status = TaskResultStatus.COMPLETED
        print("<--- COMPANIES-HOUSE-CONVERT TASK COMPLETE! --->")
        return task_result

    def get_polling_interval_in_seconds(self) -> float:
        # poll every 500ms
        return 0.5
