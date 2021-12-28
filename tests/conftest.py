import pytest
from brownie import accounts, OlympusERC20Token, OlympusTreasury, sOlympus


@pytest.fixture(scope="module")
def olympus_erc20_token():
    owner = accounts[0]
    fake_authority = accounts[1]
    return OlympusERC20Token.deploy(fake_authority, {"from": owner})


@pytest.fixture(scope="module")
def olympus_treasury(olympus_erc20_token):
    owner = accounts[0]
    fake_authority = accounts[1]
    return OlympusTreasury.deploy(
        olympus_erc20_token.address, 20, fake_authority, {"from": owner}
    )

@pytest.fixture(scope="module")
def sOlympus_token(olympus_erc20_token):
    owner = accounts[0]
    return sOlympus.deploy({'from': owner})