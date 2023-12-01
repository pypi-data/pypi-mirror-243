import os
import subprocess
from typing import Optional

import pyshorteners


def build_job_jenkins(jenkins_url=os.getenv('jenkins_url'),
                      username=os.getenv('jenkins_username'),
                      api_token=os.getenv('jenkins_api_token'),
                      job_name=os.getenv('jenkins_job_name'),
                      testkit_debug=os.getenv('testkit_debug'),
                      cdrouter_restart=os.getenv('cdrouer_restart'),
                      cdrouter_device=os.getenv('cdrouter_device'),
                      cdrouter_config=os.getenv('cdrouter_config'),
                      cdrouter_package=os.getenv('cdrouter_package'),
                      cdrouter_test=os.getenv('cdrouter_test'),
                      cdrouter_tests=os.getenv('cdrouter_tests'),
                      TicketKey=os.getenv('TicketKey'),
                      tags=os.getenv('tags'),
                      cdrouter_skipUpload=os.getenv('cdrouter_skipUpload'),
                      cdrouter_message=os.getenv('cdrouter_message')):
    """Build a Jenkins job with the specified parameters.

       Args:
           jenkins_url (str): URL of the Jenkins server. Defaults to the JENKINS_URL environment variable.
           username (str): Username for authentication. Defaults to the JENKINS_USERNAME environment variable.
           api_token (str): API token for authentication. Defaults to the JENKINS_API_TOKEN environment variable.
           job_name (str): Name of the Jenkins job to build. Defaults to the JENKINS_JOB_NAME environment variable.
           testkit_debug (str): Whether to enable testkit debug mode. Defaults to the TESTKIT_DEBUG environment variable.
           cdrouter_restart (str): Whether to restart the CDRouter system before running the test. Defaults to the CDROUER_RESTART environment variable.
           cdrouter_device (str): The name of the CDRouter test device. Defaults to the CDROUTER_DEVICE environment variable.
           cdrouter_config (str): The name of the CDRouter config file to use. Defaults to the CDROUTER_CONFIG environment variable.
           cdrouter_package (str): The name of the CDRouter test package to run. Defaults to the CDROUTER_PACKAGE environment variable.
           cdrouter_test (str): The name of the CDRouter test case to run. Defaults to the CDROUTER_TEST environment variable.
           cdrouter_tests (str): The name(s) of the CDRouter test case(s) to run. Defaults to the CDROUTER_TESTS environment variable.
           TicketKey (str): The ticket key to associate with the test results. Defaults to the TICKET_KEY environment variable.
           tags (str): The tags to associate with the test results. Defaults to the TAGS environment variable.
           cdrouter_skipUpload (str): Whether to skip uploading test results to the CDRouter web UI. Defaults to the CDROUTER_SKIP_UPLOAD environment variable.
           cdrouter_message (str): The message to associate with the test results. Defaults to the CDROUTER_MESSAGE environment variable.

       Returns:
           Tuple of stdout and stderr from the subprocess run command.
   """
    cmd = f'java -jar %userprofile%\bin\jenkins-cli.jar -s {jenkins_url} -webSocket -auth "{username}":"{api_token}" '
    cmd += f'build "{job_name}" -v '
    cmd += f'-p testkit_debug="{testkit_debug}" '
    cmd += f'-p cdrouter_restart="{cdrouter_restart}" '
    cmd += f'-p cdrouter_device="{cdrouter_device}" '
    cmd += f'-p cdrouter_config="{cdrouter_config}" '
    cmd += f'-p cdrouter_package="{cdrouter_package}" '
    cmd += f'-p cdrouter_test="{cdrouter_test}" '
    cmd += f'-p cdrouter_tests="{cdrouter_tests}" '
    cmd += f'-p TicketKey="{TicketKey}" '
    cmd += f'-p tags="{tags}" '
    cmd += f'-p cdrouter_skipUpload="{cdrouter_skipUpload}" '
    cmd += f'-p cdrouter_message="{cdrouter_message}"'

    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout, result.stderr


def generate_custom_test_url(jenkins_url: Optional[str] = os.getenv('JENKINS_URL'),
                             jenkins_api_token: Optional[str] = os.getenv('JENKINS_API_TOKEN'),
                             testkit_debug: Optional[bool] = os.getenv('testkit_debug', True),
                             cdrouter_restart: Optional[bool] = os.getenv('cdrouer_restart', False),
                             cdrouter_device: Optional[str] = os.getenv('cdrouter_device'),
                             cdrouter_config: Optional[str] = os.getenv('cdrouter_config'),
                             cdrouter_package: Optional[str] = os.getenv('cdrouter_package'),
                             cdrouter_test: Optional[str] = os.getenv('cdrouter_test'),
                             cdrouter_tests: Optional[str] = os.getenv('cdrouter_tests'),
                             TicketKey: Optional[str] = os.getenv('TicketKey'),
                             tags: Optional[str] = os.getenv('tags'),
                             cdrouter_skipUpload: Optional[bool] = os.getenv('cdrouter_skipUpload', False),
                             cdrouter_message: Optional[str] = os.getenv('cdrouter_message'),
                             use_tiny_url: Optional[bool] = os.getenv('use_tiny_url', False)) -> str:
    """Generate a custom test URL for Jenkins job execution.

        Args:
            jenkins_url (str, optional): The base URL for the Jenkins instance.
                Defaults to the value of the 'JENKINS_URL' environment variable.
            jenkins_api_token (str, optional): The API token for the Jenkins instance.
                Defaults to the value of the 'JENKINS_API_TOKEN' environment variable.
            testkit_debug (str, optional): Whether or not to enable TestKit debug mode.
                Defaults to the value of the 'testkit_debug' environment variable.
            cdrouter_restart (str, optional): Whether or not to restart CDRouter.
                Defaults to the value of the 'cdrouer_restart' environment variable.
            cdrouter_device (str, optional): The CDRouter device to use for testing.
                Defaults to the value of the 'cdrouter_device' environment variable.
            cdrouter_config (str, optional): The CDRouter configuration to use for testing.
                Defaults to the value of the 'cdrouter_config' environment variable.
            cdrouter_package (str, optional): The CDRouter package to use for testing.
                Defaults to the value of the 'cdrouter_package' environment variable.
            cdrouter_test (str, optional): The CDRouter test(s) to execute.
                Defaults to the value of the 'cdrouter_test' environment variable.
            cdrouter_tests (str, optional): The type of CDRouter tests to execute.
                Defaults to the value of the 'cdrouter_tests' environment variable.
            TicketKey (str, optional): The ticket key for the test.
                Defaults to the value of the 'TicketKey' environment variable.
            tags (str, optional): The tags to associate with the test.
                Defaults to the value of the 'tags' environment variable.
            cdrouter_skipUpload (str, optional): Whether or not to skip uploading results to Jenkins.
                Defaults to the value of the 'cdrouter_skipUpload' environment variable.
            cdrouter_message (str, optional): The message to associate with the CDRouter test run.
                Defaults to the value of the 'cdrouter_message' environment variable.
            use_tiny_url (bool, optional): Whether or not to shorten the URL using a URL shortener.
                Defaults to the value of the 'use_tiny_url' environment variable, or True if it is not set.

        Returns:
            str: The generated custom test URL.
        """
    jenkins_url_hook = f"{jenkins_url}/generic-webhook-trigger/invoke"
    jenkins_params = f"token={jenkins_api_token}&testkit_debug={testkit_debug}&cdrouter_restart={cdrouter_restart}&cdrouter_skipUpload={cdrouter_skipUpload}&TicketKey={TicketKey}&cdrouter_device={cdrouter_device}&cdrouter_config={cdrouter_config}&cdrouter_package={cdrouter_package}&cdrouter_tests={cdrouter_tests}&cdrouter_test={cdrouter_test}&cdrouter_message={cdrouter_message}&tags={tags}"
    encoded_params = jenkins_params.replace(" ", "%20")
    url = f"{jenkins_url_hook}?{encoded_params}"
    if use_tiny_url:
        s = pyshorteners.Shortener()
        url = s.tinyurl.short(url)
    return url


def generate_repeat_test_url(
        jenkins_url: Optional[str] = os.getenv('JENKINS_URL'),
        jenkins_api_token: Optional[str] = os.getenv('JENKINS_API_TOKEN'),
        use_tiny_url: Optional[bool] = os.getenv('use_tiny_url', False)) -> str:
    """
    Generates a Jenkins URL for repeating a previously executed job.

    Args:
        jenkins_url (Optional[str]): The base URL of the Jenkins server. Defaults to the value of the JENKINS_URL
            environment variable.
        jenkins_api_token (Optional[str]): The API token for authenticating with the Jenkins server. Defaults to the
            value of the JENKINS_API_TOKEN environment variable.
        use_tiny_url (Optional[bool]): Whether to use a URL shortener to shorten the generated URL. Defaults to the
            value of the use_tiny_url environment variable.

    Returns:
        str: The generated Jenkins URL.

    """
    jenkins_url_hook = f"{jenkins_url}/generic-webhook-trigger/invoke"
    jenkins_params = f"token={jenkins_api_token}"
    encoded_params = jenkins_params.replace(" ", "%20")
    url = f"{jenkins_url_hook}?{encoded_params}"
    if use_tiny_url:
        s = pyshorteners.Shortener()
        url = s.tinyurl.short(url)
    return url


def generate_cdrouter_tags_url(
        jenkins_url: Optional[str] = os.getenv('JENKINS_URL')[:-6],
        use_tiny_url: Optional[bool] = os.getenv('use_tiny_url', False),
        device_tag: Optional[str] = os.getenv('cdrouter_device'),
        config_tag: Optional[str] = os.getenv('cdrouter_config')) -> str:
    """
    Generates a URL for CDRouter test results based on the given device and config tags.

    Args:
        jenkins_url (Optional[str]): The Jenkins URL to use for the results page. If not provided,
            the value of the 'JENKINS_URL' environment variable with the last six characters removed
            will be used.
        use_tiny_url (Optional[bool]): Whether to use a short URL generated by the pyshorteners library.
            If True, the 'use_tiny_url' environment variable will be checked and the URL will be
            shortened using tinyurl.com. Defaults to False.
        device_tag (Optional[str]): The device tag to use in the URL. If not provided, the value of the
            'cdrouter_device' environment variable will be used.
        config_tag (Optional[str]): The config tag to use in the URL. If not provided, the value of the
            'cdrouter_config' environment variable will be used.

    Returns:
        str: The generated URL for the CDRouter test results page.
    """
    url = f"{jenkins_url}/results?tags={device_tag},{config_tag}"
    if use_tiny_url:
        s = pyshorteners.Shortener()
        url = s.tinyurl.short(url)
    return url
