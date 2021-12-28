import pytest
from brownie import (
    accounts,
    OlympusERC20Token,
    OlympusTreasury,
    sOlympus,
    OlympusStaking,
    gOHM,
    Distributor,
)


@pytest.fixture(scope="module")
def OHM_token():
    owner = accounts[0]
    fake_authority = accounts[1]
    return OlympusERC20Token.deploy(fake_authority, {"from": owner})


@pytest.fixture(scope="module")
def olympus_treasury(OHM_token):
    owner = accounts[0]
    fake_authority = accounts[1]
    return OlympusTreasury.deploy(
        OHM_token.address, 20, fake_authority, {"from": owner}
    )


@pytest.fixture(scope="module")
def sOHM_token():
    owner = accounts[0]
    return sOlympus.deploy({"from": owner})


@pytest.fixture(scope="module")
def gOHM_token(sOHM_token):
    owner = accounts[0]
    migrator = accounts[1]
    return gOHM.deploy(migrator, sOHM_token.address, {"from": owner})


@pytest.fixture(scope="module")
def olympus_staking_contract(OHM_token, sOHM_token, gOHM_token):
    owner = accounts[0]
    fake_authority = accounts[1]
    return OlympusStaking.deploy(
        OHM_token.address,
        sOHM_token.address,
        gOHM_token.address,
        10,
        10,
        10,
        fake_authority,
        {"from": owner},
    )


@pytest.fixture(scope="module")
def distributor_contract(olympus_treasury, OHM_token, olympus_staking_contract):
    owner = accounts[0]
    fake_authority = accounts[1]
    return Distributor.deploy(
        olympus_treasury.address,
        OHM_token.address,
        olympus_staking_contract.address,
        fake_authority,
        {"from": owner},
    )
