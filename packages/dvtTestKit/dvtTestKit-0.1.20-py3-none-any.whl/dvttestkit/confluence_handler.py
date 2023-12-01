import json
import os
from collections import namedtuple

import requests
from requests.auth import HTTPBasicAuth
from sphinx.application import Sphinx

from dvttestkit import testKitUtils

logger = testKitUtils.makeLogger(__name__, True)


def generate_pdf(doc_path, doc_index):
    """
    Generate a PDF file from a Sphinx documentation project.

    Args:
        doc_path (str): The path to the root directory of the Sphinx documentation project.
        doc_index (str): The filename of the RST index file (without the extension).
    """
    # Change to the documentation directory
    os.chdir(doc_path)

    # Build the documentation
    app = Sphinx(doc_path, doc_path, doc_path, doc_path, doc_index)
    app.build()

    # Convert the LaTeX file to PDF
    os.chdir(os.path.join(doc_path, '_build', 'latex'))
    os.system('make')

    # Move the PDF file to the documentation directory
    os.rename(os.path.join(doc_path, '_build', 'latex', f'{doc_index}.pdf'),
              os.path.join(doc_path, f'{doc_index}.pdf'))


def get_confluence_page_title(page_id: str, confluence_domain: str = os.getenv(
    "JiraDomain")) -> str:
    # Set the Confluence API endpoint and authentication credentials
    url = f"{confluence_domain}/wiki/rest/api/content/{page_id}"
    auth = HTTPBasicAuth(os.getenv("JiraEmail"), os.getenv("JiraToken"))

    # Set the headers for the API request
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the API request to get the Confluence page
    response = requests.get(url, auth=auth, headers=headers)

    # Check if the API request was successful
    if response.status_code == 200:
        # Return the title of the page
        return response.json()['title']
    else:
        # Raise an exception with the error message
        raise Exception('Error getting Confluence page: ' + response.text)


def get_confluence_page_version(page_id: str,
                                confluence_domain: str = os.getenv(
                                    "JiraDomain")):
    """
        Retrieves the version number of a Confluence page. This is used for

        Args:
            page_id (str): The ID of the Confluence page to retrieve the version number for.
            confluence_domain (str): The base URL of the Confluence site, including the protocol
                                     (e.g., 'https://your-domain.atlassian.net'). Defaults to the
                                     value of the 'JiraDomain' environment variable.

        Returns:
            The version number of the Confluence page as an integer.

        Raises:
            Exception: If an error occurs while retrieving the Confluence page version.
    """
    # Set the Confluence API endpoint and authentication credentials
    url = f"{confluence_domain}/wiki/rest/api/content/{page_id}?expand=version"
    auth = HTTPBasicAuth(os.getenv("JiraEmail"), os.getenv("JiraToken"))

    # Send the API request to retrieve the Confluence page
    response = requests.get(url, auth=auth)

    # Check if the API request was successful
    if response.status_code == 200:
        # Return the version number of the page
        return response.json()['version']['number']
    else:
        # Raise an exception with the error message
        raise Exception(
            'Error retrieving Confluence page version: ' + response.text)


def get_page_data(confluence_domain: str = os.getenv("JiraDomain"),
                  page_id: str = os.getenv("PageId")):
    """
    Makes a GET request to the Confluence API to retrieve data for the specified page.
    Returns a named tuple with the following fields: app_id, title, body, version, space, ancestors,
    status, created_date, updated_date

    :param page_id: the ID of the Confluence page
    :return: Named Tuple
    """
    response = requests.get(
        f"https://{confluence_domain}/wiki/rest/api/content/",
        auth=HTTPBasicAuth(os.getenv("JiraEmail"), os.getenv("JiraToken"))
    )
    # Check the status code of the response
    if response.status_code == 200:
        # The request was successful, so parse the response JSON and return it as a named tuple
        _data = json.loads(response.text)
        page_tuple = namedtuple(
            'page_tuple',
            ['app_id', 'title', 'body', 'version', 'ancestors', 'status', ]
        )
        return page_tuple(
            id=_data['app_id'],
            title=_data['title'],
            body=_data['body']['storage']['value'],
            version=_data['version']['number'],
            # space=_data['space']['key'],
            ancestors=[ancestor['app_id'] for ancestor in _data['ancestors']],
            status=_data['status'],
            # created_date=_data['history']['createdDate'],
            # updated_date=_data['history']['lastUpdatedDate']
        )
    else:
        # The request failed, so raise an error
        response.raise_for_status()


def create_confluence_page(title: str = "dvtTestKit",
                           conf_file_path: str = "dvtTestKit.conf",
                           confluence_domain: str = os.getenv("JiraDomain"),
                           space_key: str = os.getenv("SPACE_KEY"),
                           parent_id: str = None) -> str:
    """
    Creates a new Confluence page with the specified title and content.

    Args:
    -------
        title (str):
            | The title of the new page. Defaults to 'dvttestKit'.
        conf_file_path (str):
            | The path to the .conf file containing the content of the new page.
            | Defaults to 'dvtTestKit.conf'.
        confluence_domain (str):
            | The base URL of the Confluence site, including the protocol
            | (e.g., 'https://your-domain.atlassian.net').
            | Defaults to the value of the 'JiraDomain' environment variable.
        space_key (str):
            | The key of the space in which to create the new page. Defaults to the
            value of the 'SPACE_KEY' environment variable.
        parent_id (str):
            | The ID of the parent page, if the new page should be a child of an
              existing page. Defaults to None, meaning the new page will be created
              at the top level of the space.

    Returns
    --------
    str
        The ID of the newly created page.

    Raises
    -------
        Exception: If an error occurs while creating the Confluence page.
    """
    # Set the Confluence API endpoint and authentication credentials
    url = f"{confluence_domain}/wiki/rest/api/content/"
    auth = HTTPBasicAuth(os.getenv("JiraEmail"), os.getenv("JiraToken"))
    contents = testKitUtils.get_contents(conf_file_path)

    # Set the JSON payload for creating a new Confluence page
    payload = {
        "type": "page",
        "title": title,
        "space": {
            "key": space_key
        },
        "body": {
            "storage": {
                "value": contents,
                "representation": "storage"
            }
        }
    }

    # If a parent page ID was provided, add it to the JSON payload
    if parent_id:
        payload['ancestors'] = [{'app_id': parent_id}]

    # Convert the payload to JSON
    payload_json = json.dumps(payload)

    # Set the headers for the API request
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the API request to create the Confluence page
    response = requests.post(url, data=payload_json, auth=auth,
                             headers=headers)

    # Check if the API request was successful
    if response.status_code == 200:
        # Return the ID of the new page
        return response.json()['app_id']
    else:
        # Raise an exception with the error message
        raise Exception('Error creating Confluence page: ' + response.text)


def update_confluence_page_if_changed(page_id, conf_file_path, confluence_domain=os.getenv("JiraDomain"), space_key=os.getenv("SPACEKEY"), parent_id=None):
    """
    Updates an existing Confluence page with new content only if the content has changed.

    Args:
        page_id (str): The ID of the page to update.
        conf_file_path (str): The path to the .conf file containing the new content for the page.
        confluence_domain (str): The base URL of the Confluence site, including the protocol
                                 (e.g., 'https://your-domain.atlassian.net'). Defaults to the
                                 value of the 'JiraDomain' environment variable.
        parent_id (str): The ID of the new parent page, if the updated page should be moved to a
                         different parent page. Defaults to None, meaning the parent page will not
                         be changed.

    Returns:
        None.

    Raises:
        Exception: If an error occurs while updating the Confluence page.
    """
    # Set the Confluence API endpoint and authentication credentials
    url = f"{confluence_domain}/wiki/rest/api/content/{page_id}"
    auth = HTTPBasicAuth(os.getenv("JiraEmail"), os.getenv("JiraToken"))
    filepath = f"docs/build/confluence/{conf_file_path}.conf"
    conf_content = testKitUtils.get_contents(filepath)

    # Check if the new content is different from the existing content
    response = requests.get(url, auth=auth)
    if response.status_code != 200:
        raise Exception('Error retrieving Confluence page: ' + response.text)
    existing_content = response.json().get('body', {}).get('storage', {}).get('value', '')
    if existing_content == conf_content:
        print('The page content has not changed, skipping update.')
        return

    # Set the JSON payload for updating the Confluence page
    payload = {
        "app_id": page_id,
        "type": "page",
        "title": get_confluence_page_title(page_id),
        "space": {
            "key": space_key
        },
        "version": {
            "number": get_confluence_page_version(page_id) + 1
        },
        "body": {
            "storage": {
                "value": conf_content,
                "representation": "storage"
            }
        }
    }

    # If a parent page ID was provided, add it to the JSON payload
    if parent_id:
        payload['ancestors'] = [{'app_id': parent_id}]

    # Convert the payload to JSON
    payload_json = json.dumps(payload)

    # Set the headers for the API request
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the API request to update the Confluence page
    response = requests.put(url, data=payload_json, auth=auth, headers=headers)

    # Check if the API request was successful
    if response.status_code != 200:
        # Raise an exception with the error message
        logger.debug(f' Page: {page_id}. Error updating Confluence page: {response.text}')
        raise Exception('Error updating Confluence page: ' + response.text)

    return response.status_code



def update_confluence_page(page_id: str,
                           conf_file_path: str,
                           confluence_domain: str = os.getenv("JiraDomain"),
                           space_key: str = os.getenv("SPACE_KEY"),
                           parent_id: str = None) -> int:
    """
    Updates an existing Confluence page with new content.

    Args:
        page_id (str): The ID of the page to update.
        conf_file_path (str): The path to the .conf file containing the new content for the page.
        confluence_domain (str): The base URL of the Confluence site, including the protocol.
                                 Defaults to the value of the 'JiraDomain' environment variable.
        space_key (str): The key of the space that contains the page to update.
                         Defaults to the value of the 'SPACE_KEY' environment variable.
        parent_id (str, optional): The ID of the new parent page, if the updated page should be moved to a
                                   different parent page. Defaults to None, meaning the parent page will not be changed.

    Returns:
        str: The HTTP status code of the API response.

    Raises:
        Exception: If an error occurs while updating the Confluence page.
    """

    # Set the Confluence API endpoint and authentication credentials
    url = f"{confluence_domain}/wiki/rest/api/content/{page_id}"
    auth = HTTPBasicAuth(os.getenv("JiraEmail"), os.getenv("JiraToken"))
    if conf_file_path.endswith(".py"):
        conf_file_path = conf_file_path[:-3]
    filepath = f"docs/build/confluence/{conf_file_path}.conf"
    logger.debug(f"pre file check {filepath}")
    if os.path.isfile(filepath):
        logger.debug(f"File found: {filepath}")
        conf_content = testKitUtils.get_contents(filepath)
    else:
        logger.debug(f"not found {filepath}")
        return 0

    # Set the JSON payload for updating the Confluence page
    payload = {
        "id": page_id,
        "type": "page",
        "title": get_confluence_page_title(page_id),
        "space": {
            "key": space_key
        },
        "version": {
            "number": get_confluence_page_version(page_id) + 1
        },
        "body": {
            "storage": {
                "value": conf_content,
                "representation": "storage"
            }
        }
    }

    # If a parent page ID was provided, add it to the JSON payload
    if parent_id: payload['ancestors'] = [{'id': parent_id}]

    # Convert the payload to JSON
    payload_json = json.dumps(payload)

    # Set the headers for the API request
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the API request to update the Confluence page
    response = requests.put(url, data=payload_json, auth=auth, headers=headers)

    # Check if the API request was successful
    if response.status_code != 200:
        # Raise an exception with the error message
        logger.debug(
            f' Page: {page_id}. Error updating Confluence page: {response.text}')
        raise Exception('Error updating Confluence page: ' + response.text)
    logger.debug(f"Update successful for {filepath}")
    return response.status_code


def delete_confluence_page(page_id: str,
                           confluence_domain: str = os.getenv("JiraDomain")):
    """
    Deletes a Confluence page with the given ID using the Confluence REST API.

    Args:
        page_id (str): The ID of the Confluence page to delete.
        confluence_domain (str): The domain of the Confluence instance. Defaults to the JiraDomain environment variable.

    Raises:
        Exception: If the API request to delete the page was unsuccessful.

    Returns:
        None
    """
    # Set the Confluence API endpoint and authentication credentials
    url = f"{confluence_domain}/wiki/rest/api/content/{page_id}"
    auth = HTTPBasicAuth(os.getenv("JiraEmail"), os.getenv("JiraToken"))

    # Set the headers for the API request
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the API request to delete the Confluence page
    response = requests.delete(url, auth=auth, headers=headers)

    # Check if the API request was successful
    if response.status_code != 204:
        # Raise an exception with the error message
        raise Exception('Error deleting Confluence page: ' + response.text)


def get_child_page_ids(parent_id, confluence_domain=os.getenv("JiraDomain")):
    """
    Retrieves the page IDs of all child pages under a given parent page.

    Parameters:
    parent_id (str): The ID of the parent page.
    confluence_domain (str): The domain of the Confluence site. Default is retrieved from environment variable.

    Returns:
    list: A list of page IDs for all child pages under the given parent page.
    """
    # Set the Confluence API endpoint and authentication credentials
    url = f"{confluence_domain}/wiki/rest/api/content/{parent_id}/child/page?limit=1000"
    auth = HTTPBasicAuth(os.getenv("JiraEmail"), os.getenv("JiraToken"))

    # Set the headers for the API request
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the API request to retrieve the child pages of the parent page
    response = requests.get(url, auth=auth, headers=headers)

    # Check if the API request was successful
    if response.status_code == 200:
        # Extract the page IDs from the API response
        child_page_ids = [page['id'] for page in response.json()['results']]
        # Recursively retrieve the child pages of each child page
        for child_id in child_page_ids:
            child_page_ids.extend(get_child_page_ids(child_id))
        return child_page_ids
    else:
        # Raise an exception with the error message
        raise Exception('Error retrieving child pages: ' + response.text)


if __name__ == '__main__':
    for each in (get_child_page_ids("2751201315")):
        logger.debug(get_confluence_page_title(each))
