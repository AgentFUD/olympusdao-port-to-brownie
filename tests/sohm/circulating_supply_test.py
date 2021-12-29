import pytest


def test_circulating_supply_is_zero_when_owned_by_staking_contract(
    accounts, sohm, gohm, staker, treasury
):
    initializer = accounts[0]
    sohm.setIndex(1, {"from": initializer})
    sohm.setgOHM(gohm.address, {"from": initializer})
    sohm.initialize(staker.address, treasury.address, {"from": initializer})

    assert staker.supplyInWarmup() == 0
    assert gohm.totalSupply() == 0
    assert gohm.balanceFrom(10) == 0


def test_circulating_supply(sohm):
    assert sohm.circulatingSupply() == 0


@pytest.mark.skip
def test_includes_all_the_supply_owned_by_gohm(staker, sohm, gohm):
    assert staker.supplyInWarmup() == 0
    assert gohm.totalSupply() == 10
    assert gohm.balanceFrom(10) == 10
    assert sohm.circulatingSupply() == 10000


@pytest.mark.skip
def test_includes_all_the_supply_in_warmup_in_staker_contract(staker, sohm, gohm):
    assert 3 == 2
