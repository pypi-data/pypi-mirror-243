import re
from collections import namedtuple
from typing import Any
import json
import requests
import doctest

from dvttestkit import testKitUtils

logger = testKitUtils.makeLogger(__name__)



# def get_ticket_components(jira_domain: str = os.getenv("JiraDomain"),
#                           issue_key: str = os.getenv('TicketKey')) -> Optional[str]:
#     """
#     Retrieve the name of the components field for a given Jira ticket.
#
#     :param jira_domain: temp
#     :param issue_key: Jira ticket key (e.g. "AUTO-770")
#     :return: name of the components field, or None if the request failed
#     """
#     response = requests.get(
#         f"{jira_domain}/rest/api/2/issue/{issue_key}",
#         auth=HTTPBasicAuth(os.getenv("JiraEmail"), os.getenv("JiraToken"))
#     )
#
#     if response.status_code == 200:
#         _data = response.json()
#         return _data["fields"]["components"][0].get('name')
#     else:
#         logger.error(f"Failed to retrieve components for ticket {issue_key}: {response.text}")
#         return None


def convert(dictionary: dict) -> Any:
    """
    Convert a dictionary to a namedtuple.

    :param dictionary: input dictionary
    :return: namedtuple with keys and values from the input dictionary
    """
    for key, value in dictionary.items():
        if isinstance(value, dict):
            dictionary[key] = convert(value)
    return namedtuple('GenericDict', dictionary.keys())(**dictionary)


def custom_decoder(obj: dict) -> Any:
    """
    Convert a dictionary to a namedtuple, replacing invalid characters in keys.

    :param obj: input dictionary
    :return: namedtuple with keys and values from the input dictionary, with invalid characters in keys replaced
    """

    def replace_invalid_chars(string: str) -> str:
        return re.sub(r'\W', '_', string)

    valid_keys = [replace_invalid_chars(key) for key in obj.keys()]
    return namedtuple('X', valid_keys)(*obj.values())


# def set_status_testing(jira_domain: str = os.getenv("JiraDomain"), transition_name: str = "DVT Testing",
#                        issue_key: str = os.getenv('TicketKey')):
#     """
#     Changes the status of the specified Jira ticket to `transition_name`.
#
#     :param transition_name: The target status name to set.
#     :type transition_name: str
#     :param issue_key: The Jira ticket key.
#     :type issue_key: str
#     :return: HTTP status code of the POST request.
#     :rtype: int
#     """
#     # Get the current status of the ticket
#     ticket_data = get_ticket_data(issue_key=issue_key)
#     current_status = ticket_data.status
#     # Check if the current status is already `transition_name`
#     print(current_status)
#     if current_status == "In Review":
#         print(f"Ticket {issue_key} is already in {current_status}.")
#         return 200
#     if current_status == "Done":
#         print(f"Ticket {issue_key} is already in {current_status}.")
#         return 200
#
#     transition_id = get_ticket_transitions(transition_name=transition_name, issue_key=issue_key)
#
#     # Sending POST request
#     logger.debug(f"{os.getenv('JiraEmail')}, {os.getenv('JiraToken')}")
#     response = requests.request(
#         "POST",
#         f"{jira_domain}/rest/api/2/issue/{issue_key}/transitions",
#         headers={"Accept": "application/json", "Content-Type": "application/json"},
#         auth=HTTPBasicAuth(os.getenv('JiraEmail'), os.getenv('JiraToken')),
#         json={"transition": {"id": transition_id}}
#     )
#
#     return response.status_code


# def get_ticket_data(jira_domain: str = os.getenv("JiraDomain"), issue_key: str = os.getenv('TicketKey')):
#     """
#     Makes a GET request to the Jira API to retrieve data for the specified ticket.
#     Returns a named tuple with the following fields: key, summary, description, due_date, components,
#     status, assignee, priority, change_date, view_date
#
#     :param jira_domain: temp
#     :param issue_key: the key of the Jira ticket (e.g. "SPACE-123")
#     :return: Named Tuple
#     """
#     response = requests.get(
#         f"{jira_domain}/rest/api/2/issue/{issue_key}?detailed=true",
#         auth=HTTPBasicAuth(os.getenv("JiraEmail"), os.getenv("JiraToken"))
#     )
#     # Check the status code of the response
#     if response.status_code == 200:
#         # The request was successful, so parse the response JSON and return it as a named tuple
#         _data = json.loads(response.text)
#         ticket_tuple = namedtuple(
#             'ticket_tuple',
#             ['key', 'summary', 'description',
#              'due_date', 'components', 'status', 'assignee',
#              'priority', 'change_date', 'view_date']
#         )
#
#         key = _data.get("key")
#         summary = _data["fields"].get("summary")
#         description = _data["fields"].get("description")
#         due_date = _data["fields"].get("duedate")
#         components = _data["fields"]["components"][0].get('name')
#         status = _data["fields"]["status"].get('name')
#         assignee = _data["fields"]["assignee"].get('displayName')
#         priority = _data["fields"]["priority"].get('name')
#         change_date = _data["fields"].get("statuscategorychangedate")
#         view_date = _data["fields"].get("lastViewed")
#
#         # Return the data as a named tuple
#         return ticket_tuple(
#             key, summary, description,
#             due_date, components, status,
#             assignee, priority, change_date,
#             view_date
#         )
#     else:
#         # The request was not successful, so print the error message
#         return f"Error: {response.text}"


# def get_board_data(jira_domain: str = os.getenv("JiraDomain"), board_id: str = os.getenv('BoardKey')):
#     """
#     Makes a GET request to the Jira API to retrieve data for the specified ticket.
#     Returns  named tuple with the following fields: key, summary, description, due_date, components,
#     status, assignee, priority, change_date, view_date
#
#     :param board_id: the key of the Jira ticket (e.g. "DVT-123")
#     :return: Named Tuple
#     """
#     # Make the GET request to the /rest/api/2/issue/{issue_key} endpoint
#     response = requests.get(
#         f"{jira_domain}/rest/agile/1.0/board/{board_id}/issue?fields=status",
#         auth=HTTPBasicAuth(os.getenv("JiraEmail"), os.getenv("JiraToken"))
#     )
#     # Check the status code of the response
#     if response.status_code == 200:
#         # The request was successful, so parse the response JSON and return it as a named tuple
#         _data = json.loads(response.text)
#         ticket_tuple = namedtuple(
#             'ticket_tuple',
#             ['key', 'summary', 'description',
#              'due_date', 'components', 'status', 'assignee',
#              'priority', 'change_date', 'view_date']
#         )
#         return _data
#     else:
#         # The request was not successful, so print the error message
#         return f"Error: {response.text}"
#
#
# def retrieve_wip_tickets(jira_domain: str = os.getenv("JiraDomain"),
#                          board_id: str = 'AUTO'):
#     """
#     Retrieve Jira tickets with status 'In Progress' from Jira board 'AUTO'
#
#     Returns:
#         List of ticket summaries with status 'In Progress'
#     """
#     endpoint = f'{jira_domain}/rest/agile/1.0/board/{board_id}/issue'
#     auth = HTTPBasicAuth(os.getenv("JiraEmail"), os.getenv("JiraToken"))
#     params = {"boardId": board_id}
#     response = requests.get(endpoint, auth=auth, params=params)
#
#     if response.status_code != 200:
#         raise Exception(f"Failed to retrieve tickets: {response.status_code}")
#
#     ticket_summaries = []
#     for ticket in response.json()['issues']:
#         if ticket['fields']['status'].get('name') == 'In Progress':
#             ticket_summaries.append(ticket['fields']['summary'])
#
#     return ticket_summaries
#
#
# def parse_jira_tickets(tickets):
#     # TODO move this function back to cdrouterTestKit
#     parsed_tickets = []
#     for ticket in tickets:
#         # Split the ticket summary by hyphen
#         parts = ticket.split('-')
#
#         # Extract the device name, package version, and test type from the ticket summary
#         device = parts[0]
#         package = f"{parts[1]}-{parts[2]}-{parts[3]}"
#         test_type = parts[4]
#
#         # Set the cdrouter_device, cdrouter_package, and cdrouter_tests variables
#         ticket_dict = {
#             'cdrouter_device': device,
#             'cdrouter_package': package,
#             'cdrouter_tests': test_type
#         }
#
#         # Set the cdrouter_config variable based on the test type
#         if test_type == 'Run CDRouter Docsis Test':
#             ticket_dict['cdrouter_config'] = f'{device}_docsis'
#         elif test_type == 'Run Full IPv6 CDRouter Test':
#             ticket_dict['cdrouter_config'] = f'{device}_ipv6'
#         elif test_type == 'Run Full Automation Test':
#             ticket_dict['cdrouter_config'] = f'{device}_automation'
#         elif test_type == 'Run 2.4GHz Test':
#             ticket_dict['cdrouter_config'] = f'{device}_wifi'
#         elif test_type == 'Run 5GHz Test':
#             ticket_dict['cdrouter_config'] = f'{device}_wifi_5GHz'
#
#         parsed_tickets.append(ticket_dict)
#     return parsed_tickets
#
#
# def attach_file_to_ticket(file, jira_domain: str = os.getenv("JiraDomain"), issue_key=os.getenv('TicketKey')):
#     """
#     Attaches file to given Jira ticket
#     :type file: path
#     :param jira_domain: temp
#     :param file:
#     :type issue_key: str
#     :param issue_key:
#
#     """
#     response = requests.request(
#         "POST",
#         f"{jira_domain}/rest/api/2/"
#         f"issue/{issue_key}/attachments",
#         headers={
#             "Accept": "application/json",
#             "X-Atlassian-Token": "no-check"
#         },
#         auth=HTTPBasicAuth(os.getenv("JiraEmail"),
#                            os.getenv("JiraToken")),
#         files={
#             "file": (
#                 f"{file}",
#                 open(f"{file}", "rb"),
#                 "application-type"
#             )
#         }
#     )
#     return json.dumps(
#         json.loads(response.text),
#         sort_keys=True,
#         indent=4,
#         separators=(",", ": ")
#     )
#
#
# def get_ticket_transitions(transition_name, jira_domain: str = os.getenv("JiraDomain"),
#                            issue_key: str = os.getenv('TicketKey')):
#     # Make a GET request to the Xray API to get the test result
#     response = requests.get(
#         f"{jira_domain}/rest/api/2/issue/{issue_key}"
#         f"/transitions?expand=transitions.fields",
#         auth=HTTPBasicAuth(os.getenv("JiraEmail"),
#                            os.getenv("JiraToken"))
#     )
#     # Check the status code of the response
#     if response.status_code == 200:
#         # If the request was successful, parse the JSON response
#         transitions = response.json()["transitions"]
#         for transition in transitions:
#             if transition["name"] == transition_name:
#                 return transition["app_id"]
#     else:
#         # If the request was not successful, print an error message
#         return f"Error getting test result: {response.status_code}"
#
#
# class TicketData:
#     def __init__(self, issue_key: str = os.getenv('TicketKey')):
#         self.data = get_ticket_data(issue_key)
#
#
# def update_test_status(api_token: str, test_execution_id: str, status: str) -> requests.Response:
#     """
#     This function updates the test execution status using the Xray REST API.
#
#     Args:
#         api_token (str): The Jira API token.
#         test_execution_id (str): The id of the test execution to update.
#         status (str): The new status to set for the test execution.
#
#     Returns:
#         requests.Response: The response from the API call.
#     """
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {api_token}'
#     }
#
#     url = f'https://minimco.atlassian.net/rest/raven/1.0/api/testrun/{test_execution_id}/status'
#
#     payload = {
#         'status': status
#     }
#
#     return requests.post(url, headers=headers, data=json.dumps(payload))
#

def get_test_run_info(api_token: str, email: str, test_run_id: str) -> requests.Response:
    """
    This function retrieves information about a specific test run using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_run_id (str): The ID of the test run to retrieve.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
        >>> class MockResponse:
        ...     @staticmethod
        ...     def json():
        ...         return {'status': 'success', 'data': {'test_run_id': '123'}}
        ...     status_code = 200

        >>> def mock_get(*args, **kwargs):
        ...     return MockResponse()

        >>> requests.get = mock_get
        >>> response = get_test_run_info('dummy_token', 'example@email.com', '123')
        >>> response.json()
        {'status': 'success', 'data': {'test_run_id': '123'}}
        >>> response.status_code
        200
    """

    headers = {
            'Authorization': api_token,
            'email':         email,
            'Content-Type':  'application/json',
            'Accept':        'application/json'
            }

    url = f'https://app.qadeputy.com/api/v1/test-run/{test_run_id}'

    return requests.get(url, headers=headers)


def get_incomplete_test_runs(api_token: str, email: str, per_page: int) -> requests.Response:
    """
    This function retrieves a paginated list of incomplete test runs using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        per_page (int): Number of test runs to retrieve per page.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "data": [{"test_run_id": 201, "name": "Test Run -XX", "test_run_status": "Active", "total_test_cases_count": 3}],
    ...             "links": {"first": "http://app.qadeputy.com/api/v1/test-runs?page=1", "next": "http://app.qadeputy.com/api/v1/test-runs?page=2"},
    ...             "meta": {"current_page": 1, "per_page": "15", "total": 55}
    ...         }
    ...     status_code = 200

    >>> def mock_get(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.get = mock_get
    >>> response = get_incomplete_test_runs('dummy_token', 'example@email.com', 10)
    >>> response_json = response.json()
    >>> response_json["data"][0]["test_run_id"], response_json["meta"]["total"]
    (201, 55)
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    params = {
        'is_completed': 0,
        'pagination': True,
        'per_page': per_page,
        'page': 1
    }

    url = 'https://app.qadeputy.com/api/v1/test-runs'

    return requests.get(url, headers=headers, params=params)


def create_test_run(api_token: str, email: str, name: str, description: str, test_suite_id: int, user_ids: list, test_case_ids: list) -> requests.Response:
    """
    This function creates a new test run in the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        name (str): Name of the test run.
        description (str): Description of the test run.
        test_suite_id (int): ID of the test suite.
        user_ids (list): List of user IDs.
        test_case_ids (list): List of test case IDs.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_run_id": 668,
    ...             "name": "Test Run RX10",
    ...             "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry",
    ...             "test_suite_id": 268,
    ...             "test_suite_name": "Test Suite -- RX10",
    ...             "total_test_cases_count": 2
    ...         }
    ...     status_code = 200

    >>> def mock_post(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.post = mock_post
    >>> response = create_test_run('dummy_token', 'example@email.com', 'Test Run RX10', 'Lorem Ipsum...', 268, [22, 23], [101, 102])
    >>> response_json = response.json()
    >>> response_json["test_run_id"], response_json["total_test_cases_count"]
    (668, 2)
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'name': name,
        'description': description,
        'test_suite': test_suite_id,
        'users': user_ids,
        'include_all': False,
        'test_cases': test_case_ids
    }

    url = 'https://app.qadeputy.com/api/v1/test-runs'

    return requests.post(url, headers=headers, data=json.dumps(data))


def update_test_run(api_token: str, email: str, test_run_id: int, name: str, description: str) -> requests.Response:
    """
    This function updates an existing test run in the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_run_id (int): The ID of the test run to update.
        name (str): The new name for the test run.
        description (str): The new description for the test run.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_run_id": 668,
    ...             "name": "Test Run RX10 --updated",
    ...             "description": "Lorem Ipsum -- updated",
    ...             "total_test_cases_count": 3
    ...         }
    ...     status_code = 200

    >>> def mock_put(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.put = mock_put
    >>> response = update_test_run('dummy_token', 'example@email.com', 668, 'Test Run RX10 --updated', 'Lorem Ipsum -- updated')
    >>> response_json = response.json()
    >>> response_json["test_run_id"], response_json["name"]
    (668, 'Test Run RX10 --updated')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'name': name,
        'description': description
    }

    url = f'https://app.qadeputy.com/api/v1/test-runs/{test_run_id}'

    return requests.put(url, headers=headers, data=json.dumps(data))


def get_test_cases_for_run(api_token: str, email: str, test_run_id: int, per_page: int) -> requests.Response:
    """
    This function retrieves a list of test cases for a specific test run using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_run_id (int): The ID of the test run.
        per_page (int): Number of test cases to retrieve per page.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "data": [{"test_case_id": 18376, "name": "Test Case 1"}, {"test_case_id": 18902, "name": "Test Case 3"}],
    ...             "meta": {"current_page": 1, "total": 4}
    ...         }
    ...     status_code = 200

    >>> def mock_get(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.get = mock_get
    >>> response = get_test_cases_for_run('dummy_token', 'example@email.com', 668, 15)
    >>> response_json = response.json()
    >>> len(response_json["data"]), response_json["meta"]["total"]
    (2, 4)
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    params = {
        'pagination': True,
        'per_page': per_page,
        'page': 1
    }

    url = f'https://app.qadeputy.com/api/v1/test-runs/{test_run_id}/test-cases'

    return requests.get(url, headers=headers, params=params)


def update_test_case(api_token: str, email: str, test_run_id: int, test_case_id: int, test_case_status: int, actual_result: str) -> requests.Response:
    """
    This function updates the status and actual result of a specific test case in a test run using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_run_id (int): The ID of the test run.
        test_case_id (int): The ID of the test case to update.
        test_case_status (int): The new status for the test case.
        actual_result (str): The actual result of the test case.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "previous_value": [{"test_case_status": 1, "actual_result": None}],
    ...             "updated_value": [{"test_case_status": 2, "actual_result": "Test actual result"}]
    ...         }
    ...     status_code = 200

    >>> def mock_put(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.put = mock_put
    >>> response = update_test_case('dummy_token', 'example@email.com', 1001, 501, 2, 'Test actual result')
    >>> response_json = response.json()
    >>> response_json["updated_value"][0]["test_case_status"], response_json["updated_value"][0]["actual_result"]
    (2, 'Test actual result')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'test_case_status': test_case_status,
        'actual_result': actual_result
    }

    url = f'https://app.qadeputy.com/api/v1/test-runs/{test_run_id}/test-cases/{test_case_id}'

    return requests.put(url, headers=headers, data=json.dumps(data))


def get_custom_test_case_statuses(api_token: str, email: str, per_page: int) -> requests.Response:
    """
    This function retrieves a list of custom test case statuses from the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        per_page (int): Number of test case statuses to retrieve per page.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "data": [{"test_case_status_id": 6, "name": "Completed"}, {"test_case_status_id": 16, "name": "Reset Mode"}],
    ...             "meta": {"current_page": 1, "total": 7}
    ...         }
    ...     status_code = 200

    >>> def mock_get(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.get = mock_get
    >>> response = get_custom_test_case_statuses('dummy_token', 'example@email.com', 15)
    >>> response_json = response.json()
    >>> len(response_json["data"]), response_json["meta"]["total"]
    (2, 7)
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    params = {
        'status_type': 'custom_status',
        'pagination': True,
        'per_page': per_page,
        'page': 1
    }

    url = 'https://app.qadeputy.com/api/v1/test-case-statuses'

    return requests.get(url, headers=headers, params=params)


def update_test_suite(api_token: str, email: str, test_suite_id: int, name: str, description: str, product_id: int) -> requests.Response:
    """
    This function updates a test suite in the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_suite_id (int): The ID of the test suite to update.
        name (str): The new name for the test suite.
        description (str): The new description for the test suite.
        product_id (int): The product ID associated with the test suite.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_suite_id": 268,
    ...             "name": "Test Suite -- RX10 --update",
    ...             "description": "DESC --update",
    ...             "product_id": 27
    ...         }
    ...     status_code = 200

    >>> def mock_put(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.put = mock_put
    >>> response = update_test_suite('dummy_token', 'example@email.com', 268, 'Test Suite -- RX10 --update', 'DESC --update', 27)
    >>> response_json = response.json()
    >>> response_json["test_suite_id"], response_json["name"]
    (268, 'Test Suite -- RX10 --update')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'name': name,
        'description': description,
        'product': product_id
    }

    url = f'https://app.qadeputy.com/api/v1/test-suites/{test_suite_id}'

    return requests.put(url, headers=headers, data=json.dumps(data))


def create_test_suite(api_token: str, email: str, name: str, description: str, product_id: int) -> requests.Response:
    """
    This function creates a new test suite in the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        name (str): Name of the test suite.
        description (str): Description of the test suite.
        product_id (int): The product ID associated with the test suite.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_suite_id": 271,
    ...             "name": "test Suite --create",
    ...             "description": "lorem Ipsum",
    ...             "product_id": 27
    ...         }
    ...     status_code = 200

    >>> def mock_post(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.post = mock_post
    >>> response = create_test_suite('dummy_token', 'example@email.com', 'test Suite --create', 'lorem Ipsum', 27)
    >>> response_json = response.json()
    >>> response_json["test_suite_id"], response_json["name"]
    (271, 'test Suite --create')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'name': name,
        'description': description,
        'product': product_id
    }

    url = 'https://app.qadeputy.com/api/v1/test-suites'

    return requests.post(url, headers=headers, data=json.dumps(data))


def get_test_cases_in_suite(api_token: str, email: str, test_suite_id: int, test_case_status: str, per_page: int) -> requests.Response:
    """
    This function retrieves test cases for a specific test suite from the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_suite_id (int): The ID of the test suite.
        test_case_status (str): The status of the test cases to filter by.
        per_page (int): Number of test cases to retrieve per page.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "data": [{"test_case_id": 47228, "name": "ReportingService/GetTimeOffTypeFilter"}, {"test_case_id": 47229, "name": "ReportingService/Ping"}],
    ...             "meta": {"current_page": 1, "total": 3}
    ...         }
    ...     status_code = 200

    >>> def mock_get(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.get = mock_get
    >>> response = get_test_cases_in_suite('dummy_token', 'example@email.com', 268, 'active', 15)
    >>> response_json = response.json()
    >>> len(response_json["data"]), response_json["meta"]["total"]
    (2, 3)
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    params = {
        'test_case_status': test_case_status,
        'per_page': per_page,
        'page': 1
    }

    url = f'https://app.qadeputy.com/api/v1/test-suites/{test_suite_id}/test-cases'

    return requests.get(url, headers=headers, params=params)


def get_test_case_details(api_token: str, email: str, test_suite_id: int, test_case_id: int) -> requests.Response:
    """
    This function retrieves detailed information about a specific test case within a test suite from the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_suite_id (int): The ID of the test suite.
        test_case_id (int): The ID of the test case to retrieve details for.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_case_id": 47230,
    ...             "name": "ZenQ Test - ReportingService/GetTimeOffReport Copy",
    ...             "test_feature": "uAttend QA - Reporting API --2"
    ...         }
    ...     status_code = 200

    >>> def mock_get(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.get = mock_get
    >>> response = get_test_case_details('dummy_token', 'example@email.com', 268, 47230)
    >>> response_json = response.json()
    >>> response_json["test_case_id"], response_json["name"]
    (47230, 'ZenQ Test - ReportingService/GetTimeOffReport Copy')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    url = f'https://app.qadeputy.com/api/v1/test-suites/{test_suite_id}/test-cases/{test_case_id}'

    return requests.get(url, headers=headers)


def update_test_case_details(api_token: str, email: str, test_suite_id: int, test_case_id: int, name: str, preconditions: str, expected_results: str, test_case_steps: str, specifications: str, time: str) -> requests.Response:
    """
    This function updates details of a specific test case within a test suite using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_suite_id (int): The ID of the test suite.
        test_case_id (int): The ID of the test case to update.
        name (str): Updated name of the test case.
        preconditions (str): Updated preconditions of the test case.
        expected_results (str): Updated expected results of the test case.
        test_case_steps (str): Updated test case steps.
        specifications (str): Updated specifications URL.
        time (str): Updated time value for the test case.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_case_id": 47230,
    ...             "name": "Test Case --updated",
    ...             "preconditions": "desc",
    ...             "test_case_steps": "desc",
    ...             "expected_results": "desc",
    ...             "specifications": "https://www.example.com",
    ...             "time": "23:12"
    ...         }
    ...     status_code = 200

    >>> def mock_put(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.put = mock_put
    >>> response = update_test_case_details('dummy_token', 'example@email.com', 268, 47230, 'Test Case --updated', 'desc', 'desc', 'desc', 'https://www.example.com', '23:12')
    >>> response_json = response.json()
    >>> response_json["test_case_id"], response_json["name"]
    (47230, 'Test Case --updated')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'name': name,
        'preconditions': preconditions,
        'expected_results': expected_results,
        'test_case_steps': test_case_steps,
        'specifications': specifications,
        'time': time
    }

    url = f'https://app.qadeputy.com/api/v1/test-suites/{test_suite_id}/test-cases/{test_case_id}'

    return requests.put(url, headers=headers, data=json.dumps(data))


def create_test_case(api_token: str, email: str, test_suite_id: int, test_feature_id: int, name: str, preconditions: str, expected_results: str, test_case_steps: str, specifications: str, time: str) -> requests.Response:
    """
    This function creates a new test case in a specific test suite using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_suite_id (int): The ID of the test suite.
        test_feature_id (int): The ID of the test feature.
        name (str): Name of the test case.
        preconditions (str): Preconditions of the test case.
        expected_results (str): Expected results of the test case.
        test_case_steps (str): Test case steps.
        specifications (str): Specifications URL.
        time (str): Time value for the test case.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_case_id": 48969,
    ...             "name": "Test Case create --logo A",
    ...             "preconditions": "desc",
    ...             "test_case_steps": "desc",
    ...             "expected_results": "desc",
    ...             "specifications": "https://www.example.com",
    ...             "time": "23:12"
    ...         }
    ...     status_code = 200

    >>> def mock_post(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.post = mock_post
    >>> response = create_test_case('dummy_token', 'example@email.com', 268, 5395, 'Test Case create --logo A', 'desc', 'desc', 'desc', 'https://www.example.com', '23:12')
    >>> response_json = response.json()
    >>> response_json["test_case_id"], response_json["name"]
    (48969, 'Test Case create --logo A')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'test_feature_id': test_feature_id,
        'name': name,
        'preconditions': preconditions,
        'expected_results': expected_results,
        'test_case_steps': test_case_steps,
        'specifications': specifications,
        'time': time
    }

    url = f'https://app.qadeputy.com/api/v1/test-suites/{test_suite_id}/test-cases'

    return requests.post(url, headers=headers, data=json.dumps(data))


def add_test_case_result(api_token: str, email: str, test_case_id: int, test_case_status: int, actual_result: str, created_by_user_id: int, test_run_id: int) -> requests.Response:
    """
    This function adds a test result to a specific test case using the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_case_id (int): The ID of the test case.
        test_case_status (int): The status ID of the test case result.
        actual_result (str): The actual result of the test case.
        created_by_user_id (int): The user ID of the person who created the test result.
        test_run_id (int): The ID of the test run associated with the test case.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "test_case_id": "47230",
    ...             "test_case_name": "Test Case --updated",
    ...             "test_case_status": "Passed",
    ...             "actual_result": "test result is Passed",
    ...             "created_by": "Admin George"
    ...         }
    ...     status_code = 200

    >>> def mock_post(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.post = mock_post
    >>> response = add_test_case_result('dummy_token', 'example@email.com', 47230, 3, 'test result is Passed', 74, 754)
    >>> response_json = response.json()
    >>> response_json["test_case_id"], response_json["actual_result"]
    ('47230', 'test result is Passed')
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        'test_case_status': test_case_status,
        'actual_result': actual_result,
        'created_by_user_id': created_by_user_id,
        'test_run': test_run_id
    }

    url = f'https://app.qadeputy.com/api/v1/test-cases/{test_case_id}/test-results'

    return requests.post(url, headers=headers, data=json.dumps(data))


def get_test_case_results(api_token: str, email: str, test_case_id: int, per_page: int, current_page: int) -> requests.Response:
    """
    This function retrieves test results for a specific test case from the QA Deputy API.

    Args:
        api_token (str): The API token for authorization.
        email (str): The email associated with the API token.
        test_case_id (int): The ID of the test case.
        per_page (int): Number of results per page.
        current_page (int): The current page number for pagination.

    Returns:
        requests.Response: The response from the API call.

    Doctests:
    >>> class MockResponse:
    ...     @staticmethod
    ...     def json():
    ...         return {
    ...             "data": [{"test_case_id": 47230, "test_case_name": "Test Case --updated --new", "test_case_status": "Failed"}],
    ...             "meta": {"current_page": 1, "total": 27}
    ...         }
    ...     status_code = 200

    >>> def mock_get(*args, **kwargs):
    ...     return MockResponse()

    >>> requests.get = mock_get
    >>> response = get_test_case_results('dummy_token', 'example@email.com', 47230, 15, 1)
    >>> response_json = response.json()
    >>> len(response_json["data"]), response_json["meta"]["total"]
    (1, 27)
    >>> response.status_code
    200
    """

    headers = {
        'Authorization': api_token,
        'email': email,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    params = {
        'pagination': True,
        'per_page': per_page,
        'page': current_page
    }

    url = f'https://app.qadeputy.com/api/v1/test-cases/{test_case_id}/test-results'

    return requests.get(url, headers=headers, params=params)



# Example usage
# response = get_test_run_info('your_api_token', 'your_email', 'test_run_id_1')
# print(response.json())


if __name__ == '__main__':
    # You can now call this function like so:
    # response = update_test_status("your_api_token", "your_test_execution_id", "EXECUTING")
    doctest.testmod()
