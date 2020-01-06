from unittest.mock import Mock

from app import main


def test_print_name():
    name = 'test'
    data = {'name': name}
    req = Mock(get_json=Mock(return_value=data), args=data)

    assert main.hello_world(req) == 'Hello {}! {}'.format(name, main.SECRET_STRING)


def test_print_hello_world():
    data = {}
    req = Mock(get_json=Mock(return_value=data), args=data)

    assert main.hello_world(req) == 'Hello World! {}'.format(main.SECRET_STRING)

