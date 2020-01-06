def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'name' in request.args:
        name = request.args.get('name')
        return f'Hello {name}!'
    elif request_json and 'name' in request_json:
        name = request_json.get('name')
        return f'Hello {name}!'
    else:
        return f'Hello World!'