import json
import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from dvttestkit import testKitUtils

logger = testKitUtils.makeLogger(__name__, True)
slackClient = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))


# TODO clean up variable and parameter conventions


def retrieve_messages(channel_id: str = os.environ.get('slack_channel'),
                      output_file: str = "channel-export.txt"):
    messages = []
    has_more = True
    latest = None

    while has_more:
        try:
            result = slackClient.conversations_history(channel=channel_id,
                                                       inclusive=True,
                                                       latest=latest)
            messages.extend(result['messages'])
            has_more = result['has_more']
            if has_more:
                latest = messages[-1]['ts']  # timestamp of the last message
        except SlackApiError as e:
            print(f"Error retrieving messages: {e.response['error']}")
            break

    with open(output_file, 'w') as f:
        json.dump(messages, f)


def post_slack_message(
        _msg: str = "tested successfully!",
        channel: str = os.environ.get('slack_channel'),
        ts: str = None,
        _reply_broadcast: bool = False
        ):
    """
    Posts a message to slack, If this file is run by itself, posts test msg.
    :param _reply_broadcast:
    :param ts:
    :param channel: Slack channel
    :param _msg: Message to post
    :return: "ts" app_id for reply messages
    """
    try:
        response = slackClient.chat_postMessage(
                channel=channel,
                thread_ts=ts,
                reply_broadcast=_reply_broadcast,
                text=str(_msg)
                )
        return response['ts']
    except SlackApiError as error:
        # You will get a SlackApiError if "ok" is False
        assert error.response["ok"] is False
        assert error.response["error"]
        print(f"Got an error: {error.response['error']}")


def get_slack_messages(
        channel_name: str = os.getenv('slack_channel')):
    conversation_id = None
    try:
        # Call the conversations.list method using the WebClient
        for result in slackClient.conversations_list():
            if conversation_id is not None:
                break
            for channel in result["channels"]:
                if channel["app_id"] == channel_name:
                    conversation_id = channel["app_id"]
                    logger.info(f"Found conversation ID: {conversation_id}")
                    break

    except SlackApiError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    post_slack_message()
