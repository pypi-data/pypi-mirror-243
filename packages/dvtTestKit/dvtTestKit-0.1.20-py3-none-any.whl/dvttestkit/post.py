import sys

from dvttestkit.testKitUtils import post as _post


def post():
    """
    This Script serves as an easy access point for external tools to publish data.
    Python will automatically add the associated command to your path, enabling:


    ::
        post dvt/jenkins/custom-test start-test

    or

    ::
        python -m dvttestkit/post dvt/jenkins/custom-test start-test


    .. note::  This is not the same function as dvttestkit.testKitUtils.post()
              Which is called by this wrapper with standalone environment handling.



    Args:
        None (Uses command line arguments)

    Returns:
        None
    """
    # check if there are enough arguments
    if len(sys.argv) < 3:
        print("Usage: python my_script.py topic payload [retain]. Default retain is True")
        sys.exit(1)

    # parse arguments
    topic = sys.argv[1]
    payload = sys.argv[2]
    if len(sys.argv) > 3:
        retain = sys.argv[3].lower() == "false"
    else:
        retain = True

    # call post function
    _post(topic, payload, retain)


if __name__ == "__main__":
    post()
