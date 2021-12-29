import brownie


def test_erc20_properties(sOHM_token):
    assert sOHM_token.name() == "Staked OHM"
    assert sOHM_token.symbol() == "sOHM"
    assert sOHM_token.decimals() == 9


def test_initializer_can_set_the_index(accounts, sOHM_token):
    initializer = accounts[0]
    sOHM_token.setIndex(3, {"from": initializer})
    assert sOHM_token.index() == 3


def test_non_initializer_cannot_set_the_index(accounts, sOHM_token):
    malicious_account = accounts[1]
    with brownie.reverts():
        sOHM_token.setIndex(3, {"from": malicious_account})


def test_cannot_update_index_if_it_is_already_set(accounts, sOHM_token):
    initializer = accounts[0]
    with brownie.reverts():
        sOHM_token.setIndex(4, {"from": initializer})


def test_set_gohm_address(accounts, sOHM_token, gOHM_token):
    initializer = accounts[0]
    sOHM_token.setgOHM(gOHM_token.address, {"from": initializer})
    assert sOHM_token.gOHM() == gOHM_token.address


def test_non_initializer_cannot_set_gOHM(accounts, sOHM_token, gOHM_token):
    malicious_account = accounts[1]
    with brownie.reverts():
        sOHM_token.setgOHM(gOHM_token.address, {"from": malicious_account})


def test_gOHM_address_cannot_be_zero(accounts, sOHM_token):
    initializer = accounts[0]
    with brownie.reverts():
        sOHM_token.setgOHM(
            "0x0000000000000000000000000000000000000000", {"from": initializer}
        )


def test_initialize_assigns_total_gons_to_staking_contract(
    accounts, sOHM_token, olympus_staking_contract, olympus_treasury
):
    initializer = accounts[0]
    tx = sOHM_token.initialize(
        olympus_staking_contract.address,
        olympus_treasury.address,
        {"from": initializer},
    )
    assert sOHM_token.balanceOf(olympus_staking_contract.address) == 5000000000000000
    assert "Transfer" in tx.events.keys()
    assert "LogStakingContractUpdated" in tx.events.keys()


def test_initializer_cannot_be_called_twice(
    accounts, sOHM_token, olympus_staking_contract, olympus_treasury
):
    initializer = accounts[0]
    with brownie.reverts():
        sOHM_token.initialize(
            olympus_staking_contract.address,
            olympus_treasury.address,
            {"from": initializer},
        )
