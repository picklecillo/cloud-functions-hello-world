try:
    import function.common.api as api
    import function.common.kms as kms
except ImportError:
    import common.api as api
    import common.kms as kms


def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.  # noqa: E501
    """
    config = kms.get_config()

    request_json = request.get_json()
    if request.args and 'id' in request.args:
        issue_id = request.args.get('id')
        return api.get_single_issue(issue_id)
    elif request_json and 'id' in request_json:
        issue_id = request_json.get('id')
        return api.get_single_issue(issue_id)
    else:
        return str(config)
