import brownie
import scripts.constants as c


def test_erc20_properties(sohm):
    assert sohm.name() == "Staked OHM"
    assert sohm.symbol() == "sOHM"
    assert sohm.decimals() == 9


def test_initializer_can_set_the_index(accounts, sohm):
    initializer = accounts[0]
    sohm.setIndex(3, {"from": initializer})
    assert sohm.index() == 3


def test_non_initializer_cannot_set_the_index(accounts, sohm):
    malicious_account = accounts[1]
    with brownie.reverts():
        sohm.setIndex(3, {"from": malicious_account})


def test_cannot_update_index_if_it_is_already_set(accounts, sohm):
    initializer = accounts[0]
    with brownie.reverts():
        sohm.setIndex(4, {"from": initializer})


def test_set_gohm_address(accounts, sohm, gohm):
    initializer = accounts[0]
    sohm.setgOHM(gohm.address, {"from": initializer})
    assert sohm.gOHM() == gohm.address


def test_non_initializer_cannot_set_gOHM(accounts, sohm, gohm):
    malicious_account = accounts[1]
    with brownie.reverts():
        sohm.setgOHM(gohm.address, {"from": malicious_account})


def test_gOHM_address_cannot_be_zero(accounts, sohm):
    initializer = accounts[0]
    with brownie.reverts():
        sohm.setgOHM(
            c.ZERO_ADDRESS, {"from": initializer}
        )


def test_initialize_assigns_total_gons_to_staking_contract(
    accounts, sohm, staker, treasury
):
    initializer = accounts[0]
    tx = sohm.initialize(
        staker.address,
        treasury.address,
        {"from": initializer},
    )
    assert sohm.balanceOf(staker.address) == c.TOTAL_GONS
    assert "Transfer" in tx.events.keys()
    assert "LogStakingContractUpdated" in tx.events.keys()


def test_initializer_cannot_be_called_twice(accounts, sohm, staker, treasury):
    initializer = accounts[0]
    with brownie.reverts():
        sohm.initialize(
            staker.address,
            treasury.address,
            {"from": initializer},
        )
