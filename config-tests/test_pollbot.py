import pytest


@pytest.mark.asyncio
@pytest.mark.pollbot
async def test_product_releases(api, conf, env, apiversion):
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
    res = await api.getProductOngoingVersions(vars={"product": "devedition"})
    data = await res.json()

    assert "devedition" in data

# dict_keys(['getServerInfo', 'heartbeat', 'lbheartbeat', 'version',
# 'contribute', 'doc', 'getProductReleases',
# 'getReleaseInfoAndChecks', 'getProductOngoingVersions',
# 'checkArchiveExistance', 'checkArchivePartnerRepacks',
# 'checkCrashStatsUptake', 'checkTelemetryMainSummaryUptake',
# 'checkProductDetailsExistance',
# 'checkProductDetailsDeveditionAndBetaVersionsMatches',
# 'checkBedrockSecurityAdvisoryExistance',
# 'checkBedrockDownloadLinkExistance',
# 'checkBedrockReleaseNotesExistance', 'checkBouncerLinksVersion',
# 'checkBalrogRule', 'checkBuildhub'])


# Checking PollBot
# /firefox
# /devedition

# /firefox/ongoing-versions
# /devedition/ongoing-versions

# /firefox/{version}
# - Nightly - Try all the checks
# - Beta - Try all the checks
# - Release - Try all the checks
# - ESR - Try all the checks

# /devedition/{version}
# - Aurora - Try all the checks
