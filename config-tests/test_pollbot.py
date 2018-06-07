import requests
import time


def test_product_releases(conf, env):
    data = requests.get(conf.get(env, 'pollbot_server')).json()

    # For each product, get the product releases
    for product in data["products"]:
        res = requests.get(conf.get(env, 'pollbot_server') + '/{0}'.format(product))
        data = res.json()

        assert "releases" in data
        for release in data["releases"]:
            assert isinstance(release, str)


def test_firefox_ongoing_versions(conf, env):
    res = requests.get(conf.get(env, 'pollbot_server') + '/firefox/ongoing-versions')
    data = res.json()

    assert "nightly" in data
    assert "beta" in data
    assert "release" in data
    assert "esr" in data


def test_devedition_ongoing_versions(conf, env):
    res = requests.get(conf.get(env, 'pollbot_server') + '/devedition/ongoing-versions')
    data = res.json()

    assert "devedition" in data


def product_version_checks(conf, env, product, channel):
    res = requests.get(conf.get(env, 'pollbot_server') + "/{0}/ongoing-versions".format(product))
    data = res.json()
    current_channel_version = data[channel]

    res = requests.get(conf.get(env, 'pollbot_server') + "/{0}/{1}".format(product, current_channel_version))
    data = res.json()

    assert data["product"] == product
    assert data["version"] == current_channel_version
    assert "checks" in data

    for check in data["checks"]:
        #time.sleep(2)
        resp = requests.get(check["url"])
        body = resp.json()
        assert "status" in body
        assert body["status"] in ["exists", "incomplete", "missing", "error"]
        assert "message" in body
        assert "link" in body


def test_firefox_nightly_checks(conf, env):
    product_version_checks(conf, env, "firefox", "nightly")


def test_firefox_beta_checks(conf, env):
    product_version_checks(conf, env, "firefox", "beta")


def test_firefox_release_checks(conf, env):
    product_version_checks(conf, env, "firefox", "release")


def test_firefox_esr_checks(conf, env):
    product_version_checks(conf, env, "firefox", "esr")


def test_devedition_checks(conf, env):
    product_version_checks(conf, env, "devedition", "devedition")
