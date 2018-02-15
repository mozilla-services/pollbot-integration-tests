import aiohttp
import asyncio
import configparser
import datetime
import pkg_resources
import pytest
import sys
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

    def wrapper():
        return API(conf.get(env, api_definition), loop=event_loop)
    return wrapper


@pytest.fixture
def get_session():
    aiohttp_version = pkg_resources.get_distribution("aiohttp").version
    python_version = '.'.join([str(v) for v in sys.version_info[:3]])
    pollbot_ci_run = datetime.datetime.utcnow().isoformat()

    session_headers = {
        "User-Agent": "PollBot-CI/{} aiohttp/{} python/{}".format(
            pollbot_ci_run, aiohttp_version, python_version)
    }

    def wrapper():
        return aiohttp.ClientSession(headers=session_headers)
    return wrapper
