import pytest
from brownie import accounts, OlympusERC20Token


@pytest.fixture(scope="module")
def olympus_erc20_token():
    owner = accounts[0]
    fake_authority = accounts[1]
    return OlympusERC20Token.deploy(fake_authority, {"from": owner})
