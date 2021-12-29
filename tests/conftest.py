import pytest
from brownie import (
    accounts,
    OlympusAuthority,
    OlympusERC20Token,
    OlympusTreasury,
    sOlympus,
    OlympusStaking,
    gOHM,
    Distributor,
)


@pytest.fixture(scope="module")
def authority():
    owner = accounts[0]
    return OlympusAuthority.deploy(owner, owner, owner, owner, {"from": owner})


@pytest.fixture(scope="module")
def ohm(authority):
    owner = accounts[0]
    return OlympusERC20Token.deploy(authority.address, {"from": owner})


@pytest.fixture(scope="module")
def treasury(ohm, authority):
    owner = accounts[0]
    return OlympusTreasury.deploy(ohm.address, 20, authority.address, {"from": owner})


@pytest.fixture(scope="module")
def sohm():
    owner = accounts[0]
    return sOlympus.deploy({"from": owner})


@pytest.fixture(scope="module")
def gohm(sohm):
    owner = accounts[0]
    migrator = accounts[1]
    return gOHM.deploy(migrator, sohm.address, {"from": owner})


@pytest.fixture(scope="module")
def staker(ohm, sohm, gohm, authority):
    owner = accounts[0]
    return OlympusStaking.deploy(
        ohm.address,
        sohm.address,
        gohm.address,
        10,
        10,
        10,
        authority.address,
        {"from": owner},
    )


@pytest.fixture(scope="module")
def distributor(treasury, ohm, staker, authority):
    owner = accounts[0]
    return Distributor.deploy(
        treasury.address,
        ohm.address,
        staker.address,
        authority.address,
        {"from": owner},
    )
