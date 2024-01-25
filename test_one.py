import json
import requests
import pytest

test_url = 'https://static.gismeteo.st/assets/meta/site.webmanifest'


def get_response():
    assert requests.get(url=test_url).ok, 'Error in sending the request'
    return requests.get(url=test_url)


def get_content_type():
    content_type_param = get_response().headers.get('content-type')
    assert content_type_param is not None, 'This key is not in the response parameters'
    return content_type_param


def get_response_as_dict():
    response_as_dict = json.loads(get_response().content)
    assert isinstance(response_as_dict, dict), f'Response is not a JSON format'
    return response_as_dict


def get_key_json(data, act_keys_list):
    for key, value in data.items():
        if type(value) == type(dict()):
            get_key_json(value, act_keys_list)
        elif type(value) == type(list()):
            for val in value:
                if type(val) == type(str()):
                    pass
                elif type(val) == type(list()):
                    pass
                else:
                    get_key_json(val, act_keys_list)
        act_keys_list.append(key)


def sorting(item):
    if isinstance(item, dict):
        return sorted((key, sorting(values)) for key, values in item.items())
    if isinstance(item, list):
        return sorted(sorting(x) for x in item)
    else:
        return item


class TestOne:
    """ Какие-то тесты"""

    expected_keys_list = ["name", "short_name", "icons", "src", "sizes", "type", "theme_color", "background_color",
                          "display"]
    act_keys_list = []

    @pytest.mark.skip('Возвращается неверный формат')
    def test_check_content_type(self):
        """ Проверка, что возвращается json"""
        act_content_type = get_content_type()
        assert act_content_type == 'application/json', f'Content-type is {act_content_type}, not application/json'

    def test_checking_json_fields(self):
        """ Проверка, наличия полей"""
        get_key_json(get_response_as_dict(), TestOne.act_keys_list)
        assert set(TestOne.expected_keys_list) == set(
            TestOne.act_keys_list), f'The list of expected fields does not match'

    def test_checking_json_fields2(self):
        act_json = get_response_as_dict()
        expect_json = {
            "name": "Gismeteo",
            "short_name": "Gismeteo",
            "icons": [
                {
                    "src": "https://static.gismeteo.st/assets/meta/android-chrome-192x192.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": "https://static.gismeteo.st/assets/meta/android-chrome-256x256.png",
                    "sizes": "256x256",
                    "type": "image/png"
                }
            ],
            "theme_color": "#ffffff",
            "background_color": "#ffffff",
            "display": "standalone"
        }
        assert sorting(act_json) == sorting(expect_json), 'The returned JSON does not match the expected JSON'

