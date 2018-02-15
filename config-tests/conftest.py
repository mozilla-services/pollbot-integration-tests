import configparser
import asyncio
import pytest
from smwogger import API


@pytest.fixture
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


@pytest.fixture
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture
def api(event_loop, conf, env, request):
    api_definition = 'pollbot_api_definition'
    return API(conf.get(env, api_definition), loop=event_loop)
