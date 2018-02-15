import pytest


@pytest.mark.asyncio
@pytest.mark.pollbot
async def test_product_releases(api, conf, env, apiversion):
    async with api() as api:
        # Get products
        res = await api.getServerInfo()
        data = await res.json()

        # For each product, get the product releases
        for product in data["products"]:
            res = await api.getProductReleases(vars={"product": product})
            data = await res.json()

        assert "releases" in data
        for release in data["releases"]:
            assert isinstance(release, str)


@pytest.mark.asyncio
@pytest.mark.pollbot
@pytest.mark.firefox
async def test_firefox_ongoing_versions(api, conf, env, apiversion):
    async with api() as api:
        res = await api.getProductOngoingVersions(vars={"product": "firefox"})
        data = await res.json()

    assert "nightly" in data
    assert "beta" in data
    assert "release" in data
    assert "esr" in data


@pytest.mark.asyncio
@pytest.mark.pollbot
@pytest.mark.devedition
async def test_devedition_ongoing_versions(api, conf, env, apiversion):
    async with api() as api:
        res = await api.getProductOngoingVersions(vars={"product": "devedition"})
        data = await res.json()

    assert "devedition" in data


async def product_version_checks(api, get_session, product, channel):
    async with api() as api:
        res = await api.getProductOngoingVersions(vars={"product": product})
        data = await res.json()

        current_channel_version = data[channel]

        res = await api.getReleaseInfoAndChecks(vars={
            "product": product,
            "version": current_channel_version
        })
        data = await res.json()

    assert data["product"] == product
    assert data["version"] == current_channel_version
    assert "checks" in data

    for check in data["checks"]:
        async with get_session() as session:
            print("Testing", check["title"])
            async with session.get(check["url"]) as resp:
                body = await resp.json()
                assert "status" in body
                assert body["status"] in ["exists", "incomplete", "missing", "error"]
                assert "message" in body
                assert "link" in body


@pytest.mark.asyncio
@pytest.mark.pollbot
@pytest.mark.nightly
async def test_firefox_nightly_checks(api, conf, env, apiversion, get_session):
    await product_version_checks(api, get_session, "firefox", "nightly")


@pytest.mark.asyncio
@pytest.mark.pollbot
@pytest.mark.beta
async def test_firefox_beta_checks(api, conf, env, apiversion, get_session):
    await product_version_checks(api, get_session, "firefox", "beta")


@pytest.mark.asyncio
@pytest.mark.pollbot
@pytest.mark.release
async def test_firefox_release_checks(api, conf, env, apiversion, get_session):
    await product_version_checks(api, get_session, "firefox", "release")


@pytest.mark.asyncio
@pytest.mark.pollbot
@pytest.mark.esr
async def test_firefox_esr_checks(api, conf, env, apiversion, get_session):
    await product_version_checks(api, get_session, "firefox", "esr")


@pytest.mark.asyncio
@pytest.mark.pollbot
@pytest.mark.devedition
async def test_devedition_checks(api, conf, env, apiversion, get_session):
    await product_version_checks(api, get_session, "devedition", "devedition")
